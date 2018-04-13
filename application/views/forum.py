from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required

from application import db
from application.forms.areaform import AreaForm
from application.models.area import Area
from application.models.role import Role
from application.utils.base64util import encode64

bp = Blueprint('forum', __name__, template_folder='templates')


@bp.route("/")
def hello():
    return redirect(url_for("forum.forum_main"))


@bp.route("/forum")
def forum_main():
    areas = Area.query.all()
    return render_template("forum.html", areas=areas)


@bp.route("/area/new")
@login_required
def create_area_page():
    form = AreaForm()
    form.role.choices = [(role.id, role.name) for role in Role.query.order_by('id')]

    return render_template("forum/area_new.html", action=url_for('forum.create_area'), form=form)


@bp.route("/area/new", methods=["POST"])
@login_required
def create_area():
    form = AreaForm(request.form)

    if not form.validate():
        return render_template("forum/area_new.html", form=form)

    name = form.name.data
    description = encode64(form.description.data)

    newArea = Area(name, description, form.role.data.id)

    db.session().add(newArea)
    db.session().commit()

    return redirect(url_for("area.area", area_name=name))