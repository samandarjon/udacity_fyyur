function delete_venue(id) {
    fetch("/venues/" + id, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        },
    })
        .then(r => {
                if (r.status === 200)
                    window.location.replace('/venues');
                else
                    window.location.replace('/venues/' + id);
            }
        )
        .catch(() => window.location.replace('/artists/' + id));

}

function delete_artist(id) {
    fetch("/artists/" + id, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        },
    })
        .then(res => {
                if (res.status === 200)
                    window.location.replace('/artists');
                else
                    window.location.replace('/artists/' + id);
            }
        )
        .catch(() => window.location.replace('/artists/' + id))


}