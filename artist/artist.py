from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_paginate import get_page_parameter, Pagination

import service
from forms import ArtistForm
from models import Artist

artist = Blueprint('artist', __name__, template_folder='templates')


@artist.route('/artists')
def artists():
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page
    data = Artist.query.limit(per_page).offset(offset).all()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                            total=len(service.get_all_artists()), css_framework='bootstrap3',
                            search=search)
    return render_template('pages/artists.html', artists=data, pagination=pagination)


@artist.route('/artists/search', methods=['POST'])
def search_artists():
    search = request.form.get('search_term', '')
    artist_list = service.get_artist_by_partial_name(search)
    response = {
        "count": len(artist_list),
        "data": [
            artist.search for artist in artist_list
        ]
    }
    return render_template(
        'pages/search_artists.html',
        results=response,
        search_term=search)


@artist.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    artist = service.get_artist_by_id(artist_id)
    data = artist.complete

    return render_template('pages/show_artist.html', artist=data)


@artist.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm(request.form)
    artist = service.get_artist_by_id(artist_id)

    form.state.process_data(artist.state)
    form.genres.process_data(artist.genres)

    return render_template('forms/edit_artist.html', form=form, artist=artist)


@artist.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    if form.validate_phone(form.phone):
        try:
            service.edit_artist(
                artist_id,
                form.name.data,
                form.city.data,
                form.state.data,
                form.phone.data,
                form.genres.data,
                form.facebook_link.data,
                form.image_link.data,
                form.website.data,
                form.seeking_venue.data,
                form.seeking_description.data
            )
            flash("Artist successfully update.", 'success')
        except:
            flash("The artist was not successfully updated.", 'danger')
    else:
        flash("Phone number is not valid", 'warning')
    return redirect(url_for('artist.show_artist', artist_id=artist_id))


@artist.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    try:
        artist = service.get_artist_by_id(artist_id)
        Artist.delete(artist)
        flash('The artist has been removed together with all of its shows.', "info")
    except:
        flash('It was not possible to delete this Artist', "danger")
        return jsonify(success=False)

    return jsonify(success=True)


@artist.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@artist.route('/artists/create', methods=['POST'])
def create_artist_submission():
    form = ArtistForm(request.form)
    if form.validate_phone(form.phone):
        try:
            new_artist = Artist(
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                phone=form.phone.data,
                genres=form.genres.data,
                facebook_link=form.facebook_link.data,
                image_link=form.image_link.data,
                website=form.website.data,
                seeking_venue=form.seeking_venue.data,
                seeking_description=form.seeking_description.data
            )
            Artist.create(new_artist)
            flash('Artist ' + request.form['name'] + ' was successfully listed!', "success")
        except:
            flash('An error occurred. Artist ' + form.name +
                  ' could not be listed.', "danger")
    else:
        flash("Phone number is not valid", "warning")

    return render_template('pages/home.html')
