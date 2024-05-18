function search_element(criteria, id_number, id_type) {
    const resultsWindow = document.getElementById(id_type + "-window-" + id_number);
    const sourceInput = document.getElementById(id_type + "-input-" + id_number);
    if (criteria.length > 0) {
        resultsWindow.innerHTML = '';
        fetch(`../entry/get_${id_type}/${criteria}`)
        .then(response => response.json())
        .then(elements => {
            if (elements.length > 0) {
                resultsWindow.style.display = 'block';
                for (let i = 0; i < elements.length; i++) {
                    const value = elements[i].fields.value;
                    const node = document.createElement('div');
                    node.class = 'select-element';
                    node.innerHTML = value;
                    node.onclick = () => {
                        resultsWindow.style.display = 'none';
                        sourceInput.value = value;
                        if (id_type === 'team') {
                            populateAssignee(value);
                        }
                    };
                    resultsWindow.append(node);
                }
            }
            else {
                resultsWindow.style.display = 'none';
            }
        })
    }
    else {
        resultsWindow.style.display = 'none';
        if (id_type === 'team') {
            const assigneeSelect = document.getElementById('assignee');
            assigneeSelect.innerHTML = "";
        }
    }
}

function input_handler(element) {
    let selector_type = element.id.slice(0,4);
    let selector_number = element.id.slice(-1);
    search_element(element.value, selector_number, selector_type);
}