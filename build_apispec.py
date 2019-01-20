from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from todo.serializers import TaskSchema
import json
import os

marshmallow_plugin = MarshmallowPlugin()

spec = APISpec(
    title='Todolist API',
    version='1.0.0',
    openapi_version='2.0',
    host='api.example.com',
    info=dict(
        description='Todolist API'
    ),
    plugins=[
        marshmallow_plugin,
    ],
)

spec.definition('Task', schema=TaskSchema())
spec.add_parameter('task_id', 'path', type='integer', required=True, description='Task ID')
spec.add_parameter('q', 'query', type='string', required=False, description='Search by string')
spec.add_parameter('CreateTask', 'body', schema=marshmallow_plugin.definition_helper('CreateTask', TaskSchema()))
spec.add_parameter('UpdateTask', 'body', schema=marshmallow_plugin.definition_helper('UpdateTask', TaskSchema(partial=True)))

spec.add_path(
    path='/todo',
    operations=dict(
        get=dict(
            summary='List Tasks',
            description='List Tasks',
            parameters=['q'],
            responses={
                200: {
                    'schema': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/Task'},
                    },
                    'description': 'OK'
                }
            }
        ),
        post=dict(
            summary='Create Task',
            description='Create Task',
            parameters=['CreateTask'],
            responses={
                201: {
                    'schema': {'$ref': '#/definitions/Task'},
                    'description': 'Create Success'
                },
                400: {
                    'description': 'Validation Error'
                }
            }
        ),
    ),
)

spec.add_path(
    path='/todo/{task_id}',
    operations=dict(
        get=dict(
            summary='Get Task',
            description='Get details of Task by task_id',
            parameters=['task_id'],
            responses={
                200: {
                    'schema': {'$ref': '#/definitions/Task'},
                    'description': 'OK'
                }
            }
        ),
        post=dict(
            summary='Update Task',
            description='Update Task by task_id',
            parameters=['task_id','UpdateTask'],
            responses={
                200: {
                    'schema': {'$ref': '#/definitions/Task'},
                    'description': 'Update Success'
                },
                400: {
                    'description': 'Validation Error'
                }
            }
        ),
        delete=dict(
            summary='Delete Task',
            description='Delete Task by task_id',
            parameters=['task_id'],
            responses={
                204: {
                    'description': 'Delete Success'
                }
            }
        )
    )
)

output_path = os.path.join(os.curdir, 'docs', 'apispec.json')
with open(output_path, 'w') as fd:
    dd = json.dumps(spec.to_dict())
    fd.write(dd)
