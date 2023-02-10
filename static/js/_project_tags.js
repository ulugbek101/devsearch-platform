

export function removeTags() {
    const allTags = document.querySelectorAll('.project__tags span small i');
    allTags.forEach(tag => tag.addEventListener('click', (e) => {
        const { project: projectId, tag: tagId } = tag.parentElement.dataset;
        e.target.parentElement.parentElement.remove();
        fetch('/api/v1/remove-tag/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ projectId, tagId })
        })
            .then(response => response.json())
            .then(response => {
                const deleted = response.deleted;
                if (deleted == 'false') return;
            })
    }));
};

export function projectTags() {
    const tagField = document.querySelector('#id_tags');
    const tagsContainer = document.querySelector('.project__tags');

    if (tagField) {
        tagField.addEventListener('keyup', (e) => {
            if (e.key === ' ' || e.key === ',') {
                const tag = e.target.value;
                const project = e.target.dataset.project;
                fetch('/api/v1/add-tag/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ tag, project }),
                })
                    .then(response => response.json())
                    .then(response => {
                        const { tag, project_id, created } = response;
                        if (created == 'false') return;
                        const htmlElement = `
                        <span class="tag tag--pill tag--main">
                            <small data-project="${project_id}" data-tag="${tag.id}">
                                ${tag.name}
                                <i class="bi bi-x-lg"></i>
                            </small>
                        </span>
                        `
                        tagsContainer.innerHTML += htmlElement
                        removeTags();
                    })
                e.target.value = '';
            }
        })
    }
};







