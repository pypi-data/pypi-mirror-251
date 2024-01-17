#!/usr/bin/env python
# coding: utf-8
import re
import requests
from typing import List, Dict
from .logger import logger


class ClustroAI:

    def __init__(self, api_key: str, debug: bool = False, verbose: bool = False, verify: bool = True, timeout=60):
        """
        api_key sign up clustro ai generator
        debug debug mode
        verbose is true will print logger
        """
        self._api_key = api_key
        self._verbose = verbose
        self._timeout = timeout
        self._verify = verify

        if debug:
            self._base_url = "https://staging.clustro.ai/api"
        else:
            self._base_url = "https://api.clustro.ai"

    @property
    def api_key(self) -> str:
        return self._api_key

    def _send_request(self, method, path, data=None):
        """
        send request
        """
        headers = {'X-API-Key': self.api_key, "Content-Type": 'application/json'}
        response = requests.request(method, f'{self._base_url}/{path}', headers=headers, json=data,
                                    timeout=self._timeout, verify=self._verify)

        response.reason = response.text
        response.raise_for_status()
        if self._verbose:
            logger.debug(f"request headers {headers}")
            logger.debug(f"request data {data}")
            logger.debug(response.json())
        return response.json()

    def create_model(self, name: str, model_type: str, model_code_version: str, model_code_repo_url: str, entry_point_function: str):
        """
        name model name
        model_type the model type must be text_to_text, text_to_image, text_to_blob
        model_code_version
        waring : We only allow users with the 'admin' role to create model

        example {
            "name": "Test_Model",
            "model_type": "text_to_text",
            "model_code_version": "7a3e7912c114cec6e833a7afb9a77304b1402926",
            "model_code_repo_url": "https://github.com/ClustroAI/dummy_model_1_llm",
            "entry_point_function": "model_invoke.py/invoke"
        }
        """
        assert re.match(r"^[a-zA-Z0-9_-]+$", name), "Invalid name format"
        assert model_type in ("text_to_text", "text_to_image", "text_to_blob"), "invalid model type"
        assert re.match(r"^[a-fA-F0-9]{40}$", model_code_version) is not None, "Expected a git SHA."
        assert re.match(r"^[a-zA-Z0-9_\-]+\.py/[a-zA-Z0-9_\-]+$",
                        entry_point_function), "Expected file.py/function_name format."
        assert re.match(r"https?://[^/]+/[^/]+/[^/]+(/)?$", model_code_repo_url), "Expected a git repo URL"

        payload = {
            "name": name,
            "model_type": model_type,
            "model_code_version": model_code_version,
            "model_code_repo_url": model_code_repo_url,
            "entry_point_function": entry_point_function
        }
        return self._send_request('POST', 'models', payload)

    def list_models(self) -> List[Dict[str, str]]:
        """
        list all models
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        return self._send_request('GET', 'models')

    def get_model(self, model_id: str) -> Dict[str, str]:
        """
        get a model
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert model_id is not None
        return self._send_request('GET', f'models/{model_id}')

    def update_model(self, model_id: str, **kwargs):
        """
        update a model
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert model_id is not None
        return self._send_request('PUT', f'models/{model_id}', kwargs)

    def delete_model(self, model_id: str):
        """
        delete a model
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert model_id is not None
        return self._send_request('DELETE', f'models/{model_id}')

    def list_public_models(self, username: str = "") -> List[Dict[str, str]]:
        """
        list all public models or username public models
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        path = "public_models"
        if username:
            path += f"/{username}"
        return self._send_request('GET', path)

    def get_public_models(self, username: str, model_name: str) -> Dict[str, str]:
        """
        get the name is model name public models
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert username is not None
        assert model_name is not None
        return self._send_request('GET', f"public_models/{username}/{model_name}")

    def list_inference_jobs(self) -> List[Dict[str, str]]:
        """
        list all inference jobs
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        return self._send_request('GET', 'inference_jobs')

    def get_inference_job(self, inference_job_id: str) -> Dict[str, str]:
        """
        get inference job
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert inference_job_id is not None
        return self._send_request('GET', f'inference_jobs/{inference_job_id}')

    def update_inference_job(self, inference_job_id: str, **kwargs):
        """
        update inference job
        waring : We only allow users with the 'admin' role to update model
        """
        assert inference_job_id is not None
        return self._send_request('PUT', f'inference_jobs/{inference_job_id}', kwargs)

    def delete_inference_job(self, inference_job_id: str):
        """
        delete inference job
        waring : We only allow users with the 'admin' role to delete model
        """
        assert inference_job_id is not None
        return self._send_request('DELETE', f'inference_jobs/{inference_job_id}')

    def create_inference_job(self, model_id: str, name: str, **kwargs):
        """
        model_id the model id
        name inference job name
        kwargs other parameters
             status
             description
             min_workers
             max_workers
             desired_workers
             set_as_model_default

        waring : We only allow users with the 'admin' role to create inference_job

        example {
            "model_id": "9d1a93eb-0c6e-46ff-9014-f265ab04c7bd",
            "name": "test job"
        }
        """
        assert model_id is not None and name is not None

        payload = {
            "model_id": model_id,
            "name": name,
            **kwargs
        }
        return self._send_request('POST', 'inference_jobs', payload)

    def list_tasks(self) -> List[Dict[str, str]]:
        """
        list all tasks
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        return self._send_request('GET', 'tasks')

    def get_task(self, task_id: str) -> Dict[str, str]:
        """
        get a task
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert task_id is not None
        return self._send_request('GET', f'tasks/{task_id}')

    def list_worker(self) -> List[Dict[str, str]]:
        """
        list all workers
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        return self._send_request('GET', 'workers')

    def get_worker(self, worker_id: str) -> Dict[str, str]:
        """
        get a worker
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 60 calls per minute
        """
        assert worker_id is not None
        return self._send_request('GET', f'workers/{worker_id}')

    def update_worker(self, worker_id: str, **kwargs):
        """
        update a worker
        waring : We only allow users with the 'admin' role to update worker
        """
        assert worker_id is not None
        return self._send_request('PUT', f'workers/{worker_id}', kwargs)

    def delete_worker(self, worker_id: str):
        """
        delete a worker
        waring : We only allow users with the 'admin' role to delete worker
        """
        assert worker_id is not None
        return self._send_request('DELETE', f'workers/{worker_id}')

    def create_worker(self, name: str = None, worker_type: str = None, job_assignment_type: str = None,
                      available_gpu_memory: int = None):
        """
        name the worker name if not None else random name
        worker_type worker type  temp or longlive
        job_assignment_type job assignment type manual or auto
        available_gpu_memory worker available_gpu_memory number
        waring : We only allow users with the 'admin' role to create worker
        """
        payload = {}
        if worker_type:
            assert worker_type in ('temp', 'longlive'), "worker_type must in temp or longlive"
            payload['type'] = worker_type

        if job_assignment_type:
            assert job_assignment_type in ('manual', 'auto'), "job_assignment_type must in manual or auto"
            payload['job_assignment_type'] = job_assignment_type

        if available_gpu_memory:
            assert isinstance(available_gpu_memory, int), "available_gpu_memory must be integer"
            payload['type'] = worker_type

        if name:
            payload['name'] = name
        return self._send_request('POST', 'workers', payload)

    def run(self, input: str, model_id_or_name: str = None, job_id: str = None, sync: bool = False):
        """
        run job
        @param:input run job must input a message example: A majestic lion jumping from a big stone at night
        @params:model_id_or_name may be model_id or model_name
        @param:job_id create inference_job return the inference_job_id
        @params:sync if True will return run model results immediately
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 10 calls per minute

        result: {
                  "created_at": "Fri, 15 Sep 2023 20:36:26 GMT",
                  "task_id": "a6e5b263-b695-4ad7-8956-74251da86b7c",
                  "process_finish_time": "Fri, 15 Sep 2023 20:36:59 GMT",
                  "process_start_time": "Fri, 15 Sep 2023 20:36:26 GMT",
                  "processed_by_worker": "worker_hailongpc",
                  "result": "https://cdn.clustro.ai/generated-data/a6e5b263-b695-4ad7-8956-74251da86b7c.png"
                }
        """
        assert input is not None, "input must not be None"
        assert (model_id_or_name is not None) or (job_id is not None), \
            "Both model_id_or_name and job_id are None"

        path = ""
        if model_id_or_name:
            path = f"models/{model_id_or_name}/run_sync" if sync else f"models/{model_id_or_name}/run"
        elif job_id:
            path = f"inference_jobs/{job_id}/run_sync" if sync else f"inference_jobs/{job_id}/run"

        return self._send_request('POST', path, {"input": input})

    def username_run(self, input: str, username, model_name, sync: bool = False):
        """
        run a model by username
        waring: When users who are not in the 'admin' role call this API, we limit its usage to 10 calls per minute
        @param:input run job must input a message example: A majestic lion jumping from a big stone at night
        @param:username  register cluster ai username
        @param:model_name the name of the model
        @param:sync whether to sync, sync will return the result immediately
        result: {
                  "created_at": "Fri, 15 Sep 2023 20:36:26 GMT",
                  "task_id": "a6e5b263-b695-4ad7-8956-74251da86b7c",
                  "process_finish_time": "Fri, 15 Sep 2023 20:36:59 GMT",
                  "process_start_time": "Fri, 15 Sep 2023 20:36:26 GMT",
                  "processed_by_worker": "worker_hailongpc",
                  "result": "https://cdn.clustro.ai/generated-data/a6e5b263-b695-4ad7-8956-74251da86b7c.png"
                }
        """
        assert input is not None, "input must not be None"
        assert username is not None, "username must not be None"
        assert model_name is not None, "model_name must not be None"

        path = f"public_models/{username}/{model_name}/run"
        if sync:
            path = f"{path}_sync"
        return self._send_request('POST', path, {"input": input})
