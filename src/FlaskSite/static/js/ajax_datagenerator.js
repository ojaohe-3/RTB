// fetch data
debug = false;

function requestData() {
    $.ajax({
        type: 'GET',
        url: '/data',
        success :(data) => {
            updateData(data);
            if(debug)
                $('#debug').text(data)
        }
    })
        .then(function () {
        setTimeout(requestData, 50) //call itself every 50ms
    });
}
function requestStructureData() {
      $.ajax({
        type: 'GET',
        url: '/data/structure',
        success :(data) => {
            updateStructureData(data);
            if(debug)
                $('#debug').text(data)
        }
    });
}

function requestActivity() {
      $.ajax({
        type: 'GET',
        url: '/data/activity',
        success :(data) => {
            updateActivityData(data);
            if(debug)
                $('#debug').text(data)
        }
    }).then(function () {
          setTimeout(requestActivity,500);
      });
}
requestData();
requestStructureData();
requestActivity();