#!/usr/bin/env python3

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from client import BaseClient
from .helpers import pick
from .typing import SyncAsync
from dataclasses import dataclass

class Endpoint:

    def __init__(self, parent: "BaseClient") -> None:
        self.parent = parent


@dataclass
class Task:
    task_id: str
    project_id: str
    title: str
    content: str
    desc: str
    start_date: str
    due_date: str
    priority: int
    status: int


class TasksEndpoint(Endpoint):

    def list(self, project_id: str) -> SyncAsync[Any]:
        '''
        反馈某个Project的所有任务

        Args:
            project_id (str): _description_

        Returns:
            SyncAsync[Any]: 返回一个任务列表
        '''
        tasks= self.parent.request(
            path=f'project/{project_id}/tasks',
            method='GET',
        )
        for i in tasks:
            yield Task(task_id=i.get('id'),
                        project_id=i.get('projectId'),
                        title=i.get('title'),
                        content=i.get('content'),
                        desc=i.get('desc'),
                        start_date=i.get('startDate'),
                        due_date=i.get('dueDate'),
                        priority=i.get('prioroty'),
                        status=i.get('status'))
    
    def create(self, 
               project_id, 
               title :str, 
               content :str=None, 
               tags :list=None, 
               priority :int=1, 
               start_date: str=None, 
               end_date: str=None,
               status: int=0):
        '''
        _summary_

        Args:
            project_id (_type_): _description_
            title (str): _description_
            content (str, optional): _description_. Defaults to None.
            tags (list, optional): _description_. Defaults to None.
            priority (int, optional): _description_. Defaults to 1.
            start_date (str, optional): _description_. Defaults to None.
            status: 0 进行中, 2已完成

        Returns:
            _type_: _description_
        '''
        api = '/batch/task'

        json = {
                "add":[
                    {
                        "items":[],
                        "reminders":[],
                        "exDate":[],
                        "priority": priority,
                        "assignee": "null",
                        "progress":0,
                        "startDate": start_date,
                        "status": status,
                        "projectId": project_id,
                        "title": title,
                        "tags": tags,
                        "content": content,
                        "completedTime": end_date
                    }
                ],
                "update":[],
                "delete": [],
                "addAttachments":[],
                "updateAttachments":[],
                "deleteAttachments":[]
            }

        return self.parent.request(
            path=f'batch/task',
            method='POST',
            json=json
        )

    def get(self, task_id, project_id):
        return self.parent.request(
            path=f'task/{task_id}?projectId={project_id}',
            method='GET',
        )

    def update(self, task_id, project_id, tags: list=None, content: str=None):
        task = self.get(task_id=task_id, project_id=project_id)

        if tags:
            try:
                task['tags'] + tags
            except KeyError:
                task['tags'] = tags
 
        task['content'] = task['content'] + content

        json = {
                "add":[],
                "update":[task],
                "delete":[],
                "addAttachments":[],
                "updateAttachments":[],
                "deleteAttachments":[]
                }
        return self.parent.request(
            path='batch/task',
            method='POST',
            body=json
        )

