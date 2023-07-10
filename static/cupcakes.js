const BASE_URL = 'http://localhost:5000/api'

// Use data from cupcake to generate HTML

function generateCupcakeHTML(cupcake) {
    `
    <div data-cupcake-id=${cupcake.id}>
    <li>
    ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating}
    <button class="delete-cupcake">X</button>
    </li>
    <img class="Cupcake-img"
            src="${cupcake.image}"
            alt="(no image provided)">
    </div>
    `;
}

// Show list of cupcakes
async function ShowListCupcake() {
    const response = await axios.get(`${BASE_URL}/cupcakes`);

    for (let cupcakeData of response.data.cupcakes) {
        let newCupcake = $(generateCupcakeHTML(cupcakeData));
        $('#cupcakes-list').append(newCupcake);
    }

}



// handle data for adding cupcake form
$("#new-cupcake-form").on("submit", async function (evt) {
    evt.preventDefault();

    let flavor = $("#cupcake-flavor").val();
    let rating = $("#cupcake-rating").val();
    let size = $("#cupcake-size").val();
    let image = $("#cupcake-image").val();

    const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor,
        rating,
        size,
        image
    });

    let newCupcake = $(generateCupcakeHTML(newCupcakeResponse.data.cupcake));
    $('#cupcake-list').append(newCupcake);
    $("#new-cupcake-form").trigger("reset");
});

// handle deleteing cupcake

$("#cupcakes-list").on("click", ".delete-cupcake", async function (evt) {
    evt.preventDefault();
    let $cupcake = $(evt.target).closest("div");
    let cupcakeId = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
    $cupcake.remove();
});

$(ShowListCupcake);