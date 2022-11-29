const slide = document.querySelector(".slide");
let slideWidth = slide.clientWidth;
const prevBtn = document.querySelector(".slide_prev_button");
const nextBtn = document.querySelector(".slide_next_button");
const slideItems = document.querySelectorAll(".slide_item");
const maxSlide = slideItems.length;
let currSlide = 1;
const pagination = document.querySelector(".slide_pagination");
const progress = document.querySelector('#progress_bar');
progress.setAttribute('style', `width:${(currSlide/maxSlide)*100}%`);
const radio_1 = document.querySelector("#social_label");
const radio_2 = document.querySelector("#club_label");


nextBtn.addEventListener("click", () => {
  currSlide++;
  if (currSlide <= maxSlide) {
    progress.setAttribute('style', `width:${(currSlide/maxSlide)*100}%`)
    const offset = slideWidth * (currSlide - 1);
    slideItems.forEach((i) => {
      i.setAttribute("style", `left: ${-offset}px`);
    });
  } else {
    currSlide--;
  }
});

prevBtn.addEventListener("click", () => {
  currSlide--;
  if (currSlide > 0) {
    progress.setAttribute('style', `width:${(currSlide/maxSlide)*100}%`)
    const offset = slideWidth * (currSlide - 1);
    slideItems.forEach((i) => {
      i.setAttribute("style", `left: ${-offset}px`);
    });
  } else {
    window.history.back()
  }
});

window.addEventListener("resize", () => {
  slideWidth = slide.clientWidth;
});
// 소셜링, 클럽 소셜링 선택
radio_1.addEventListener("click", () => {
  radio_1.classList.add('active')
  radio_2.classList.remove('active')
});
radio_2.addEventListener("click", () => {
  radio_2.classList.add('active')
  radio_1.classList.remove('active')
});
// 태그 이벤트 _ 다른 카테고리 선택시 현재 선택된 태그 해제
const tags = document.querySelectorAll('div.accordion-body > .tag-btn');
let tag_input = document.querySelector('#tag')
console.log(tag_input)
var n_tag = null;
[].forEach.call(tags, function(tag){
	tag.addEventListener("click", () => {
    for (let j=0; j<(tags.length); j++){
      tags[j].classList.remove('tag-btn-active')
    }
  tag.classList.add('tag-btn-active')
  n_tag = tag;
  tag_input.value = tag.value
  }); 
}); 
// 카테고리 이벤트 _ 카테고리 선택
const categories = document.querySelectorAll('.categories');
[].forEach.call(categories, function(category){ 
	category.addEventListener("click", () => {
    for (let j=0; j<(categories.length); j++){
      categories[j].classList.remove('active')
    }
  category.classList.add('active')
  n_tag.classList.remove('tag-btn-active')
  tag_input.value = ''
  });
});
