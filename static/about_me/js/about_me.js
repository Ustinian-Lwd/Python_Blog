$("#starlist li:first-child a").attr("id", "");

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