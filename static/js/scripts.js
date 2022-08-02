// let headerHeight = $('.header').innerHeight();

// function footerFix() {
// 	headerHeight = $('.header').innerHeight();
// 	$('body').css('padding-top', headerHeight + 'px');
// }

// $(window).on('load resize', footerFix);

$(window).on('scroll load', function () {
	$(this).scrollTop() > 200
		? $('#top').addClass('active')
		: $('#top').removeClass('active');
});

$('label[for="id_remember"]').on('click', function () {
	$(this).toggleClass('active');
	if ($(this).hasClass('active')) {
		$(this).next('input').attr('checked', true)
	} else {
		$(this).next('input').attr('checked', false)
	}
})

$('#top').click(function () {
	$('body, html').animate({ scrollTop: 0 }, 500);
});

var commentsSlider = new Swiper('.book-comments.swiper-container', {
	loop: false,
	slidesPerView: 2,
	autoHeight: true,
	spaceBetween: 20,
	navigation: {
		nextEl: '.book-comments-button-next.swiper-button-next',
		prevEl: '.book-comments-button-prev.swiper-button-prev',
	},
	scrollbar: {
		el: ".book-comments-swiper-scrollbar.swiper-scrollbar",
		hide: false,
		draggable: true
	},
	breakpoints: {
		320: { slidesPerView: 1, },
		768: { slidesPerView: 2, },
	},
});

var bookmarksSlider = new Swiper('.bookmarks.swiper-container', {
	loop: false,
	slidesPerView: 8,
	autoHeight: true,
	spaceBetween: 20,
	navigation: {
		nextEl: '.bookmarks-button-next.swiper-button-next',
		prevEl: '.bookmarks-button-prev.swiper-button-prev',
	},
	scrollbar: {
		el: ".bookmarks-swiper-scrollbar.swiper-scrollbar",
		hide: false,
		draggable: true
	},
	breakpoints: {
		320: { slidesPerView: 2, },
		576: { slidesPerView: 3, },
		768: { slidesPerView: 4, },
		992: { slidesPerView: 6, },
		1200: { slidesPerView: 8, },
	},
});

$(document).on("submit", ".books__item .book__info-form", function (e) {
	e.preventDefault();
	const form = $(this);
	const checkbox = form.find('input[type="checkbox"]');
	const icon = form.find('button i');
	$.ajax({
		type: 'POST',
		url: form.attr('action'),
		data: form.serialize(),
		success: function (json) {
			(checkbox.attr('checked'))
				? (checkbox.attr('checked', false), icon.attr('class', 'far fa-bookmark'))
				: (checkbox.attr('checked', true), icon.attr('class', 'fas fa-bookmark'))
		},
		error: function (xhr, errmsg, err) {
			console.log(xhr.status + ": " + xhr.responseText);
		}
	});
});

$(document).on("submit", ".book-comments-form", function (e) {
	e.preventDefault();
	const form = $(this);
	$.ajax({
		type: 'POST',
		url: form.attr('action'),
		data: form.serialize(),
		success: function () {
			form.trigger('reset');
			$.magnificPopup.close();
			$.magnificPopup.open({
				items: { src: $('.modal_comment') },
				type: 'inline',
			}, 0);
		},
		error: function (xhr, errmsg, err) {
			console.log(xhr.status + ": " + xhr.responseText);
		}
	});
});

$('.books__item-image-link').magnificPopup({
	type: 'image',
	closeOnContentClick: true,
	mainClass: 'mfp-img-mobile',
	image: { verticalFit: true }
});

// var tooltipSlider = document.getElementById('year-slider');
// let min_year = +tooltipSlider.dataset.min_year
// let max_year = +tooltipSlider.dataset.max_year

// noUiSlider.create(tooltipSlider, {
// 	start: [min_year, max_year],
// 	tooltips: wNumb({decimals: 0}),
// 	connect: true,
// 	step: 1,
// 	range: {
// 		'min': min_year,
// 		'max': max_year
// 	}
// });
