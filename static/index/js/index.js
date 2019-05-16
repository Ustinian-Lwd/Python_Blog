// 登录注册传值
function login_register_session_storage(login_register_key) {
    // 存入一个值
    sessionStorage.setItem('login_register_key', login_register_key);
}

// 收藏喜欢传值
function collect_like_session_storage(collect_like_key) {
    // 存入一个值
    sessionStorage.setItem('collect_like_key', collect_like_key);

}




// {#  广告位的轮播图js  #}
var swiper = new Swiper('.swiper-container', {
    // 开启环路
    loop: true,
    // 自动播放
    autoplay: {
        // 时间间隔
        delay: 3500,
        // 用户操作swiper之后，是否禁止autoplay
        disableOnInteraction: false,
    },

    // 切换方式
    effect: 'cube',
    // cube效果
    cubeEffect: {
        slideShadows: true,
        shadow: true,
        shadowOffset: 15,
        shadowScale: 0.80
    },

    // 分页器
    pagination: {
        el: '.swiper-pagination',
        clickable: true,
    },
});
