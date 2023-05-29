async function init() {
    let data = await getRequest("/api/canteens")
    let blocks = "";
    for (let i = 0; i < data.length; i++) {
        let canteen = data[i];
        blocks += `
            <div class="container text-center" style="border: solid 1px; margin-top: 25px">
  <div class="row g-2">
    <div class="col-6">
      <img src="${canteen.avatar}" width="150px" style="margin-top: 10px">
    </div>
    <div class="col-6">
      <div class="p-3">
<h5>${canteen.name}</h5>
<p>${canteen.address}</p>
<p>${canteen.description}</p>
<a href="${canteen.current_menu}"><p>Меню</p></a>
      </div>
    </div>
  </div>
</div>
        `
    }

    let canteens = document.getElementById("canteens")
    canteens.innerHTML = blocks;
}

init();