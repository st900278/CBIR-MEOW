$(document).ready(function () {
    document.getElementById("upload").addEventListener("change", function () {
        var files = this.files;
        for (var i = 0; i < files.length; i++) {
            document.getElementById("preview").file = files[i];

            var reader = new FileReader();
            reader.onload = (function (aImg) {
                return function (e) {
                    aImg.src = e.target.result;
                };
            })(document.getElementById('preview'));
            reader.readAsDataURL(files[i]);

        }
    });
    document.getElementById("send_image").addEventListener("click", function () {
        document.forms["myform"].submit();

    });
});
