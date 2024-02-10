$(".gallery__items").slick({
  speed: 500,
  slidesToShow: 4,
  slidesToScroll: 4,
  infinite: true,
  autoplay: true,
  autoplaySpeed: 2000,
  responsive: [
    {
      breakpoint: 900,
      settings: {
        slidesToShow: 1,
        slidesToScroll: 1,
      },
    },
  ],
});
