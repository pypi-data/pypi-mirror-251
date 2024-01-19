import zipfile
import requests
import random
import time
import json
import copy
import os
from typing import List, Dict, Union, Tuple
import pandas as pd
import io

import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from plotly.graph_objs.layout import Colorscale

import threed_optix.package_utils.api as au
import threed_optix.package_utils.general as gu
import threed_optix.package_utils.vars as v

class RayTable(pd.DataFrame):

    def __init__(self, ray_table_url, maps_url, setup_object):
        df = au._map_ray_table(ray_table_url, maps_url)
        super().__init__(df)
        self.attrs['setup'] = setup_object
        return None

    @property
    def setup(self):
        return self.attrs['setup']

class Analysis:

    def __init__(self,
                 surface,
                 resolution: Union[Tuple[int, int], List[int]],
                 rays: dict,
                 name: str,
                 fast: bool=False):
        """
        Initializes a new instance of the Analysis class.

        Args:
            surface (Surface): The surface of the analysis.
            resolution (tuple): The resolution of the analysis surface in the form (x, y).
            rays (dict): A dictionary of lasers and the number of rays for each laser.
            name (str): The name of the analysis.
            fast (bool, optional): Specifies if the analysis is fast or advanced. Defaults to False.

        Returns:
            tdo.Analysis: The created Analysis object.

        Raises:
            AssertionError: If the name or rays are not valid for 'fast' choice.
        """

        def verify(fast, name, num_rays, surface):
            '''
            Private.
            '''

            if surface.__class__.__name__ != 'Surface':
                raise TypeError(f'surface must be of type Surface, got {surface.__class__.__name__}')

            errors = []

            if fast:
                #Check if the name of the analysis is valid for fast analysis
                if not name in v.FAST_ANALYSIS_NAMES:
                    errors.append(f"Valid names for fast analysis are {v.FAST_ANALYSIS_NAMES}")
                if not all([num <= 200 for num in num_rays]):
                    errors.append(f'Number of rays must be less than 200 for fast analysis')
            else:
                #Check if the name of the analysis is valid for advanced analysis
                if not name in v.ANALYSIS_NAMES:
                    errors.append(f"Valid names for advanced analysis are {v.ANALYSIS_NAMES}")

            #res is 2 floats tuple
            if len(resolution) != 2:
                errors.append(f'Resolution must be a tuple of 2 integers, got len {len(resolution)}')

            #Res in range
            if not all([v.ANALYSIS_RES_RANGE[0] < num <= v.ANALYSIS_RES_RANGE[1] for num in resolution]):
                errors.append(f'Resolution must be between {v.ANALYSIS_RES_RANGE[0]} and {v.ANALYSIS_RES_RANGE[1]} for analysis')

            # Rays in range
            if not all([v.ANALYSIS_RAYS_RANGE[0] <= num <= v.ANALYSIS_RAYS_RANGE[1] for num in num_rays.values()]):
                errors.append(f'Number of rays must be between {v.ANALYSIS_RAYS_RANGE[0]} and {v.ANALYSIS_RAYS_RANGE[1]} for analysis')

            # Rays values are integers
            # Trust me, Don't check for ints, because 1e8 is a float, for example
            if not all([int(num) == num for num in num_rays.values()]):
                errors.append(f'Number of rays must be an integer')

            # Rays keys are LightSource
            if not all([key.__class__.__name__ == 'LightSource' for key in num_rays.keys()]):
                errors.append(f'Keys of rays must be of type LightSource')

            return errors

        errors = verify(fast=fast, name=name, num_rays=rays, surface = surface)
        if errors:
            raise AssertionError(v.argument_repair_message(errors))

        self._added = False
        self._urls = []
        self._fail_message = None
        self._raw_results = {}
        self.results = {}
        self.surface = surface
        self.name = name
        self.rays = rays
        self.resolution = resolution
        self.id = Analysis._generate_id()
        self.fast = fast


    @classmethod
    def _new(cls, surface, resolution, num_rays, name, type, id):
        '''
        Private.
        Past analysis are stored within the setup.
        When the setup is fetched, the past analysis are created using this method.
        '''

        analysis = object.__new__(cls)
        analysis.surface = surface
        analysis.resolution = list(resolution.values())
        analysis.rays = {surface._part._setup[laser_id]: num for laser_id, num in num_rays.items()}
        analysis.name = name
        analysis.fast = False if type == '1' else True
        analysis.id = id
        analysis._added = True
        analysis._urls = []
        analysis._fail_message = None
        analysis._raw_results = {}
        analysis.results = {}

        return analysis

    @property
    def wls(self):
        '''
        Returns a sorted list of the analysis wavelengths.
        '''
        return self._analysis_wls()

    @classmethod
    def _generate_id(cls):
        '''
        Private
        Generates a unique id for the analysis.
        '''
        int_time = int(time.time())
        enc_36_time = np.base_repr(int_time, 36)
        randint = np.base_repr(random.randint(0, 36**5), 36)[2:5]
        id_ = enc_36_time + randint
        return id_

    def _analysis_wls(self):
        '''
        Private.
        Returns a sorted list of the wavelengths of the analysis
        '''
        analysis_wls = []
        setup = self.surface._part._setup
        laser_objects = [setup[laser.id] for laser in self.rays.keys()]
        for laser in laser_objects:
            wls_dicts = laser.data['light_source']['wavelengths_data']
            wls = [wls_dict['wavelength'] for wls_dict in wls_dicts]
            analysis_wls += wls
        analysis_wls = sorted(list(set(analysis_wls)))
        return analysis_wls

    def _extract_file(self,url, destination):
        ''''
        Private.
        Extracts a zip file from a url to a destination folder
        '''
        response = requests.get(url)
        if response.status_code == 200:
            zip_data = BytesIO(response.content)
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                zip_ref.extractall(destination)

        file_name = url.split('/')[-1].replace(f'{self.id}_', '').replace('.zip', '')
        file_path = f'{destination}/{file_name}'
        return file_path

    def _unpack(self):
        '''
        Private.
        Unpacks the results of the analysis to a folder
        '''
        setup = self.surface._part._setup.id
        destination_path = f'.analysis-files/{setup}/{self.surface.id}/{self.id}'
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        for url in self._urls:
            self._extract_file(url, destination_path)

        return destination_path

    def _read_file(self, file_path):
        '''
        Private.
        Reads the results of the analysis from a file
        '''
        with open(file_path, 'rb') as f:
            content = f.read()
        header_format = v.ANALYSIS_HEADER_DTYPES
        header = np.frombuffer(content[:v.HEADER_BYTES], dtype=header_format)
        data = np.frombuffer(content[v.HEADER_BYTES:], dtype=v.ANALYSIS_MATRIX_DTYPES)
        return header, data

    def _process_results(self):
        '''
        Private.
        Processes the results of the analysis
        '''
        directory = self._unpack()
        for file in os.listdir(directory):
            file_results = {}
            file_path = f'{directory}/{file}'
            headers_nums, data = self._read_file(file_path)
            headers = gu.process_headers(headers_nums)
            file_results['metadata'] = headers
            data_matrices = data.reshape(len(self.wls), self.resolution[0], self.resolution[1])
            file_results['data'] = {}
            for i, wl in enumerate(self.wls):
                matrix = data_matrices[i]
                file_results['data'][wl] = matrix
            file_name = file.split('.')[0]
            self._raw_results[file_name] = file_results
            polarized_dict = gu.reorganize_analysis_results_dict(self._raw_results.values())
        self.results = polarized_dict
        #delete directory and all subdirectories
        os.system(f'rm -rf {directory}')
        return self.results

    def __str__(self):
        json_dict = {
            "id": self.id,
            "name": self.name,
            "surface": self.surface.id,
            "rays": {laser.id: num for laser, num in self.rays.items()},
            "resolution": tuple(self.resolution),
        }
        string = json.dumps(json_dict, indent=4)
        return string

    def __eq__(self, other):
        '''
        Equal analyses are analyses with the same parameters of rays, name, resolution and surface.
        '''
        if not isinstance(other, Analysis):
            return False

        is_rays_equal = self.rays == other.rays
        is_name_equal = self.name == other.name
        is_resolution_x_equal = self.resolution[0] == other.resolution[0]
        is_resolution_y_equal = self.resolution[1] == other.resolution[1]
        is_surface_equal = self.surface.id == other.surface.id

        if is_rays_equal and is_name_equal and is_surface_equal and is_resolution_x_equal and is_resolution_y_equal:
            return True

        return False

    @property
    def data(self):
        return self.results

    def show(self, polarizations: list = None, wavelengths: list = None, figsize: Tuple[int, int] = (20, 20), upscale: bool = False):
        '''
        Shows a static figure of the analysis results.
        Args:
            figsize (tuple): The size of the figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.

        Returns:
            None

        Shows:
            A figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''
        #3DOptix color scale
        cmap = LinearSegmentedColormap.from_list('custom', v.COLOR_SCALE)

        if not self.results:
            raise Exception('Analysis was not run yet')

        if not polarizations:
            one_wl_data = list(self.results.values())[0]
            polarizations = list(one_wl_data.keys())
        if not wavelengths:
            wavelengths = list(self.results.keys())

        #Check if the analysis was run
        if not self.results:
            raise Exception('Analysis was not run yet')

        #Get the number of polarizations and wavelengths of the analysis- polarizations are the rows and wavelengths are the columns of the presented figure
        num_polarizations = len(self.results)
        num_wavelengths = len(self.wls)
        fig = plt.figure(constrained_layout=True, figsize=figsize)
        subfigs = fig.subfigures(nrows=num_polarizations, ncols=1)

        if num_polarizations == 1:
            subfigs = [subfigs]

        for polarization, subfig in zip(polarizations, subfigs):

            subfig.suptitle(f'Polarization {polarization}')
            axs = subfig.subplots(nrows=1, ncols=num_wavelengths)

            if num_wavelengths == 1:
                axs = [axs]

            for wavelength, ax in zip(wavelengths, axs):
                data = self.results[wavelength][polarization]
                if upscale:
                    dpi = plt.rcParams['figure.dpi']
                    data = gu.upscale(data, figsize[0]*dpi, figsize[1]*dpi)
                ax.imshow(data, cmap=cmap)

                ax.set_title(f'Wavelength {wavelength} nm')

        #Show the figure
        plt.show()
        return None

    def show_interactive(self, polarizations: list = None, wavelengths: list = None, figsize: Tuple[int, int] = (20, 20), upscale: bool = False):
        '''
        Shows an interactive figure of the analysis results.
        Args:
            polarizations (list): The polarizations to present. If None, all polarizations are presented.
            wavelengths (list): The wavelengths to present. If None, all wavelengths are presented.
            height (int): The height of the each figure.
            width (int): The width of each figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.
        Returns:
            None

        Shows:
            An interactive figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''
        dpi = plt.rcParams['figure.dpi']
        height = figsize[0]*dpi
        width = figsize[1]*dpi

        if not self.results:
            raise Exception('Analysis was not run yet')

        if not polarizations:
            one_wl_data = list(self.results.values())[0]
            polarizations = list(one_wl_data.keys())
        if not wavelengths:
            wavelengths = list(self.results.keys())

        for polarization in polarizations:
            for wavelength in wavelengths:
                data = self.results[wavelength][polarization]
                if upscale:
                    data = gu.upscale(data, height, width)

                fig = px.imshow(data, title=f'Polarization {polarization} Wavelength {wavelength} nm', color_continuous_scale = v.COLOR_SCALE)
                fig.update_layout(height=height, width=width)
                fig.show()

    def copy(self):
        '''
        Copies the analysis to a different analysis object with a different id.
        Returns:
        tdo.Analysis: The copied analysis.
        '''
        copied = copy.deepcopy(self)
        copied.id = Analysis._generate_id()
        copied._added = False
        return copied

    # def __call__(self, auto_add = False, force = False):
    #     self.surface._part._setup._api.run_analysis(self, force = force, auto_add = auto_add)
    #     results = copy.deepcopy(self.results)
    #     return results
