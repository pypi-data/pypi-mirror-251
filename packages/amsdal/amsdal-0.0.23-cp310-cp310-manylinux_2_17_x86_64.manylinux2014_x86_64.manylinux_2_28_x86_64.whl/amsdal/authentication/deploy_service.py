import base64
import json
import shutil
import tempfile
from pathlib import Path

import httpx
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from pydantic import BaseModel

from amsdal.authentication.handlers.base import BASE_AUTH_URL
from amsdal.authentication.handlers.base import ENCRYPT_PUBLIC_KEY
from amsdal.configs.main import settings
from amsdal.errors import AmsdalDeployError


def _input(msg: str) -> str:
    return input(msg).strip()


def _print(msg: str) -> None:
    print(msg)  # noqa: T201


def want_deploy_input() -> str:
    return _input('Do you want to deploy your app? (y/N): ')


DEPLOY_API_TIMEOUT = 60


class DeployModel(BaseModel):
    deploy_id: str
    status: str


class DeployService:
    @classmethod
    def _credentials_data(cls) -> bytes:
        key = serialization.load_pem_public_key(ENCRYPT_PUBLIC_KEY.encode())
        return key.encrypt(  # type: ignore[union-attr]
            json.dumps(
                {
                    'amsdal_access_key_id': settings.ACCESS_KEY_ID,
                    'amsdal_secret_access_key': settings.SECRET_ACCESS_KEY,
                }
            ).encode('utf-8'),
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
        )

    @classmethod
    def deploy_prompt(cls) -> bool:
        _print('Welcome to Amsdal Framework!')
        want_to_signup = want_deploy_input()

        if want_to_signup.lower() != 'y':
            return False

        with tempfile.TemporaryDirectory() as temp_dir:
            app_dir = Path(temp_dir) / 'app'
            shutil.copytree('src', app_dir / 'src')
            shutil.copy('requirements.txt', app_dir / 'requirements.txt')

            shutil.make_archive('app', 'zip', temp_dir)

        with open('app.zip', 'rb') as f:
            _data = base64.b64encode(f.read()).decode('utf-8')

        Path('app.zip').unlink(missing_ok=True)

        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/CreateAppDeploy/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'zip_archive': _data,
            },
            timeout=DEPLOY_API_TIMEOUT,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Cannot deploy service: {response.text}'
            raise AmsdalDeployError(msg)

        deploy_object = response.json()

        if deploy_object['status'] == 'failed':
            _print('Deploy failed! Please try again later.')
            return False

        client_id = deploy_object['client']['ref']['object_id']

        _print('Deploy is in progress now. After a few minutes, you can check the status of your deploy.')
        _print(f'Your API domain: https://client-{client_id}.sandbox.amsdal.com/')

        return True

    @classmethod
    def list_deploys(cls) -> list[DeployModel]:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/ListDeploys/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
            },
            timeout=DEPLOY_API_TIMEOUT,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Cannot list deploys: {response.text}'
            raise AmsdalDeployError(msg)

        return [
            DeployModel(deploy_id=deploy['_metadata']['address']['object_id'], status=deploy['status'])
            for deploy in response.json()
        ]

    @classmethod
    def update_deploy(cls, deploy_id: str) -> DeployModel:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/CheckDeployStatus/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'deploy_id': deploy_id,
            },
            timeout=DEPLOY_API_TIMEOUT,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Cannot update deploy: {response.text}'
            raise AmsdalDeployError(msg)

        deploy = response.json()

        return DeployModel(deploy_id=deploy['_metadata']['address']['object_id'], status=deploy['status'])

    @classmethod
    def destroy_deploy(cls, deploy_id: str) -> bool:
        encrypted_data = cls._credentials_data()
        response = httpx.post(
            f'{BASE_AUTH_URL}/api/transactions/DestroyAppDeploy/',
            json={
                'data': base64.b64encode(encrypted_data).decode('utf-8'),
                'deploy_id': deploy_id,
            },
            timeout=DEPLOY_API_TIMEOUT,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f'Cannot destroy deploy: {response.text}'
            raise AmsdalDeployError(msg)

        return True
