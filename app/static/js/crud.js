function createCourse(event, course_year, semester_id) {
    itemList = event.target.closest('ol');
    const newItem = document.createElement('li');
    const newItemInput = document.createElement('input');
    newItem.classList.add('rename');
    newItemInput.type = 'text'; 
    newItemInput.value = 'Name';
    newItemInput.name = 'course_name';
    newItemInput.onfocus = function() {
        newItemInput.select();
    };
    newItem.appendChild(newItemInput);
    const lastItem = itemList.querySelector('li.create');
    itemList.insertBefore(newItem, lastItem);
    newItemInput.focus();
    newItemInput.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            newItem.remove();
            return
        } else if (event.key === 'Enter') {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/create_course';
            const yearInput = document.createElement('input');
            yearInput.type = 'hidden';
            yearInput.name = 'course_year';
            yearInput.value = course_year;
            form.appendChild(yearInput);
            const semesterInput = document.createElement('input');
            semesterInput.type = 'hidden';
            semesterInput.name = 'semester_id';
            semesterInput.value = semester_id;
            form.appendChild(semesterInput);
            form.appendChild(newItemInput);
            form.classList.add('hidden');
            document.body.appendChild(form);
            form.submit();
        }
    });
}
function createSemester(event) {
    itemList = event.target.closest('ol');
    const newItem = document.createElement('li');
    const newItemInput = document.createElement('input');
    newItem.classList.add('rename');
    newItemInput.type = 'text'; 
    newItemInput.value = 'Name';
    newItemInput.name = 'semester_name';
    newItemInput.onfocus = function() {
        newItemInput.select();
    };
    newItem.appendChild(newItemInput);
    const lastItem = itemList.querySelector('li.create');
    itemList.insertBefore(newItem, lastItem);
    newItemInput.focus();
    newItemInput.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            newItem.remove();
            return
        } else if (event.key === 'Enter') {
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/create_semester';
            form.appendChild(newItemInput);
            form.classList.add('hidden');
            document.body.appendChild(form);
            form.submit();
        }
    });
}

function createExercise(lecture_id) {
    const lecture = document.createElement('input');
    lecture.name = 'lecture_id';
    lecture.value = lecture_id;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/create_exercise';
    form.appendChild(lecture);
    form.classList.add('hidden');
    document.body.appendChild(form);
    form.submit();
}

function createLecture(course_id) {
    const course = document.createElement('input');
    course.name = 'course_id';
    course.value = course_id;
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/create_lecture';
    form.appendChild(course);
    form.classList.add('hidden');
    document.body.appendChild(form);
    form.submit();
}

function renameItem(event) {
    item = event.target.closest('li')
    id = item.dataset.itemId;
    type = item.dataset.itemType;
    const placeholder = item.querySelector('.name').textContent.replace(/[\r\n]+/g, '').trim();
    const newItem = document.createElement('li');
    const newItemInput = document.createElement('input');
    newItem.classList.add('rename');
    newItemInput.type = 'text'; 
    newItemInput.value = placeholder;
    newItemInput.name = 'new_name';
    newItemInput.onfocus = function() {
        newItemInput.select();
    };
    newItem.appendChild(newItemInput);
    item.replaceWith(newItem);
    newItemInput.focus();
    newItemInput.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            newItem.replaceWith(item);
            return
        } else if (event.key === 'Enter') {
            type = item.dataset.itemType;
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/save_${type}`;
            const idInput = document.createElement('input');
            idInput.type = 'hidden';
            idInput.name = `${type}_id`;
            idInput.value = id;
            form.appendChild(idInput);
            form.appendChild(newItemInput);
            form.classList.add('hidden');
            document.body.appendChild(form);
            form.submit();
        }
    });
}
function deleteItem(event) {
    item = event.target.closest('li');
    id = item.dataset.itemId;
    type = item.dataset.itemType;
    const name = item.querySelector('.name').textContent.replace(/[\r\n]+/g, '').trim();
    const isConfirmed = window.confirm(`Are you sure you want to delete ${type} ${name}?`);
    if (isConfirmed) {
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = `/delete_${type}`;
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = `${type}_id`;
        input.value = id;
        form.appendChild(input);
        document.body.appendChild(form);
        form.submit();
    }
}