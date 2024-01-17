#!/usr/bin/env python3

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from client import BaseClient
from .helpers import pick
from .typing import SyncAsync


class Endpoint:

    def __init__(self, parent: "BaseClient") -> None:
        self.parent = parent


class TasksEndpoint(Endpoint):

    def list(self, project_id: str) -> SyncAsync[Any]:
        '''
        反馈某个Project的所有任务

        Args:
            project_id (str): _description_

        Returns:
            SyncAsync[Any]: 返回一个任务列表
        '''
        return self.parent.request(
            path=f'project/{project_id}/tasks',
            method='GET',
        )
    
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


