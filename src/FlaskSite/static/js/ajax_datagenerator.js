// fetch data
$(function requestData() {
    $ajax({
        type : 'GET',
        url: '/data',
        success : updateData(data),

    }).then(function () {
        setTimeout(requestData, 50) //call itself every 50ms
    });
})();
