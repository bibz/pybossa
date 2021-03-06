# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2014 SF Isle of Man Limited
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.

from sqlalchemy.exc import IntegrityError

from pybossa.model.project import Project
from pybossa.model.category import Category
from pybossa.exc import WrongObjectError, DBIntegrityError


class ProjectRepository(object):


    def __init__(self, db):
        self.db = db


    # Methods for Project objects
    def get(self, id):
        return self.db.session.query(Project).get(id)

    def get_by_shortname(self, short_name):
        return self.db.session.query(Project).filter_by(short_name=short_name).first()

    def get_by(self, **attributes):
        return self.db.session.query(Project).filter_by(**attributes).first()

    def get_all(self):
        return self.db.session.query(Project).all()

    def filter_by(self, limit=None, offset=0, **filters):
        query = self.db.session.query(Project).filter_by(**filters)
        query = query.order_by(Project.id).limit(limit).offset(offset)
        return query.all()

    def save(self, project):
        self._validate_can_be('saved', project)
        try:
            self.db.session.add(project)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            raise DBIntegrityError(e)

    def update(self, project):
        self._validate_can_be('updated', project)
        try:
            self.db.session.merge(project)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            raise DBIntegrityError(e)

    def delete(self, project):
        self._validate_can_be('deleted', project)
        project = self.db.session.query(Project).filter(Project.id==project.id).first()
        self.db.session.delete(project)
        self.db.session.commit()


    # Methods for Category objects
    def get_category(self, id=None):
        if id is None:
            return self.db.session.query(Category).first()
        return self.db.session.query(Category).get(id)

    def get_category_by(self, **attributes):
        return self.db.session.query(Category).filter_by(**attributes).first()

    def get_all_categories(self):
        return self.db.session.query(Category).all()

    def filter_categories_by(self, limit=None, offset=0, **filters):
        query = self.db.session.query(Category).filter_by(**filters)
        query = query.order_by(Category.id).limit(limit).offset(offset)
        return query.all()

    def save_category(self, category):
        self._validate_can_be('saved as a Category', category, klass=Category)
        try:
            self.db.session.add(category)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            raise DBIntegrityError(e)

    def update_category(self, new_category, caller="web"):
        self._validate_can_be('updated as a Category', new_category, klass=Category)
        try:
            self.db.session.merge(new_category)
            self.db.session.commit()
        except IntegrityError as e:
            self.db.session.rollback()
            raise DBIntegrityError(e)

    def delete_category(self, category):
        self._validate_can_be('deleted as a Category', category, klass=Category)
        self.db.session.query(Category).filter(Category.id==category.id).delete()
        self.db.session.commit()


    def _validate_can_be(self, action, element, klass=Project):
        if not isinstance(element, klass):
            name = element.__class__.__name__
            msg = '%s cannot be %s by %s' % (name, action, self.__class__.__name__)
            raise WrongObjectError(msg)
