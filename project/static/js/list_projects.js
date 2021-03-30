// Tag FILTERING !!

const search_btn = document.getElementById("search_btn");
const search_input = document.getElementById("search");
const f_container = document.getElementById("f-container");
search_btn.addEventListener("click", search);

function search(event) {
  value = search_input.value;

  fetch(
    `http://127.0.0.1:8000/filter_tag_or_title/?format=json&search=${value}`
  )
    .then(onResponse)
    .then(onJsonReady);
}

function onResponse(response) {
  return response.json();
}

function onJsonReady(json) {
  projects = [];
  if (json.length > 0) {
    f_container.innerHTML = " ";
    json.forEach((project) => {
      if (projects.includes(project.project)) {
        //    project already is here
      } else {
        projects.push(project.project);

        let f_item = document.createElement("div");
        f_item.classList.add("flex-item");

        let img = document.createElement("img");
        img.classList.add("flex-item-image");
        img.src = project.first_picture;
        f_item.appendChild(img);

        let h5 = document.createElement("h5");
        h5.classList.add("text-capitalize");
        h5.classList.add("text-center");
        h5.classList.add("my-2");

        let a = document.createElement("a");
        a.classList.add("no-decor");
        a.href = `../project/${project.project}/`;
        a.textContent = project.title;
        h5.appendChild(a);
        f_item.appendChild(h5);

        f_container.appendChild(f_item);
      }
    });
  }
}

// Category FILTERING !!

const categories = document.querySelectorAll(".cats");
categories.forEach((category) => {
  category.addEventListener("click", getProjects);
});

function getProjects(cat) {
  let query = cat.target.textContent;
  fetch(
    `http://127.0.0.1:8000/filter_by_category/?format=json&category__title=${query}`
  )
    .then(onResponse)
    .then(onProjectsJsonReady);
}

function onProjectsJsonReady(json) {
  console.log(json);
  if (json.length > 0) {
    f_container.innerHTML = " ";
    json.forEach((project) => {
      let f_item = document.createElement("div");
      f_item.classList.add("flex-item");

      let img = document.createElement("img");
      img.classList.add("flex-item-image");
      img.src = project.first_picture;
      f_item.appendChild(img);

      let h5 = document.createElement("h5");
      h5.classList.add("text-capitalize");
      h5.classList.add("text-center");
      h5.classList.add("my-2");

      let a = document.createElement("a");
      a.classList.add("no-decor");
      a.href = `../project/${project.pk}/`;
      a.textContent = project.title;
      h5.appendChild(a);
      f_item.appendChild(h5);

      f_container.appendChild(f_item);
    });
  }
}
