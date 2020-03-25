from app import api, Resource, fields, TaskModel
from models.TaskModel import task_schema, tasks_schema

# namespaces
ns_tasks = api.namespace('tasks', description='All tasks regarding tasks')

# models
a_task_model = api.model('Task', {
    'title': fields.String(),
    'description': fields.String(),
    'user_id' : fields.Integer()
})


@ns_tasks.route('')
class TasksList(Resource):
    def get(self):
        """ use this endpoint to get a list of tasks """
        return tasks_schema.dump(TaskModel.fetch_all()), 200

    @api.expect(a_task_model)
    def post(self):
        """ use this endpoint to add new tasks """
        data = api.payload
        task = TaskModel(**data)
        record = task.create_record();
        return task_schema.dump(record), 201


@ns_tasks.route('/<int:_id>')
class Task(Resource):
    def get(self, _id):
        """retrieve a task by it's id"""
        tasks = TaskModel.fetch_all()

        record = next(filter(lambda x: x._id == _id, tasks), None)
        if record:
            return task_schema.dump(record), 200
        else:
            return {"message": "Task does not exist"}, 404

    @api.expect(a_task_model)
    def put(self, _id):
        """edit a task by it's id"""
        data = api.payload
        task = TaskModel.fetch_by_id(_id)
        if task:
            if u'title' in data:
                task.title = data['title']
            if u'description' in data:
                task.description = data['description']
            task.save_to_db()
            return task_schema.dump(task), 200
        return 'Task does not exist', 404

    def delete(self, _id):
        """delete a task by it's id"""
        task = TaskModel.fetch_by_id(_id)
        if task:
            task.delete_from_db()
            return {'message': 'task successfully deleted'}, 200
        else:
            return {'message': 'task does not exist'}, 404
