vaptcha({
  vid: "5e428bc557272d3b8e7c1e26",
  type: "click",
  scene: 0,
  container: "#vaptchaContainer",
  offline_server: "",
  color: '#66ccff'
}).then(function (vaptchaObj) {
  obj = vaptchaObj;
  vaptchaObj.render();
  vaptchaObj.listen("pass", function () {
    // vaptcha == ok
    var data = {
      alert("OK");console.log("Vaptcha:ok");
    };
  });
  vaptchaObj.listen("close", function () {
  });
});
$('#option li').click(function() {
            $(this).addClass('active').siblings().removeClass('active');
            var a = $(this).index();
            $('#card li:eq(' + a + ')').addClass('active').siblings().removeClass('active');
        })
        
        $(".icon_e").click(function() {
            $(".captcha_count_b").show();
            $(".captcha_count_a").hide();
        })
        $(".icon_z").click(function() {
            $(".captcha_count_a").show();
            $(".captcha_count_b").hide();
        })
        console.log("Load:ok");
