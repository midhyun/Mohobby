const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
dayjs.extend(window.dayjs_plugin_relativeTime)
dayjs.extend(window.dayjs_plugin_utc)
dayjs.extend(window.dayjs_plugin_timezone)
dayjs.locale('ko')
dayjs.tz.setDefault('Asia/Seoul', true)
console.log(dayjs.tz('2022-12-05T00:00'))
console.log(dayjs.tz.guess())
const commentInput = document.querySelector('#commentinput')

const submitComment = function (e) {
    event.preventDefault();
    const commentForm = document.querySelector(`#${e}`)
    const pk = event.target.dataset.hobbyId;

    axios({
        method: 'post',
        url: `/hobby/${pk}/comment_create`,
        headers: { 'X-CSRFToken': csrftoken},
        data: new FormData(commentForm)
    })
    .then(response => {
        const commentList = document.querySelector('#comment-list')
        commentList.textContent = ""
        for (let i=0; i < response.data.comments_data.length; i++){
            let isLike = ""
            if (response.data.comments_data[i].is_like === true) {
              isLike = "heart"
            } else if (i == 7) {
              break;
            } else {
              isLike = "heart-outline"
            }
            commentList.insertAdjacentHTML('beforeend', `<hr>
            <div class="d-flex justify-content-between">
            <div class="comment-elem" >
                <img class="comment-image" src="https://dummyimage.com/80x80/000/fff" alt="">
              <div>
                <p>${ response.data.comments_data[i].user }</p>
                <p>${ response.data.comments_data[i].content }</p>
                <div>
                  <p class="text-muted" style="font-size:12px"><span>${dayjs.tz(response.data.comments_data[i].created_at).fromNow()}</span> <span>좋아요 <span id="comment-${response.data.comments_data[i].pk}-likecnt">${response.data.comments_data[i].likeCount}</span>개</span> <span>답글달기</span> <ion-icon name="ellipsis-horizontal"></ion-icon></p>
                </div>
              </div>
            </div>
            <div>
              <ion-icon id="comment-${response.data.comments_data[i].pk}-likebtn" onclick="likeComment(this)" class="comment-like-btn" data-comment-id="${response.data.comments_data[i].pk}" style="color:#E84545" name=${isLike}></ion-icon>
            </div>
            </div>`
            )}
        commentInput.value = ""

    })

}

const likeBtn = document.querySelector('.hobby-like-btn')
const likeHobby = function (e) {
  
  const hobbyPk = e.dataset.hobbyId
  axios({
    method: 'get',
    url: `/hobby/${hobbyPk}/like_hobby`,
  })
  .then(response => {
    console.log(response.data)
    if (response.data.is_like === true ) {
      likeBtn.setAttribute('name', 'heart')
    } else {
      likeBtn.setAttribute('name', 'heart-outline')
    }
    const likeCount = document.querySelector('#like-count')
    likeCount.innerText = response.data.likeCount
  })
}

const likeComment = function (e) {
  const commentPk = e.dataset.commentId
  const likeBtnComment = document.querySelector(`#comment-${commentPk}-likebtn`)
  const likeBtnCommentOff = document.querySelector(`#comment-${commentPk}-likebtn-off`)
  console.log(commentPk)
  axios({
    method: 'get',
    url: `/hobby/${commentPk}/like_comment`,
  })
  .then(response => {
    console.log(response.data)
    if (response.data.is_like === true ) {
      likeBtnComment.setAttribute('name', 'heart')
      likeBtnCommentOff.setAttribute('name', 'heart')
    } else {
      likeBtnComment.setAttribute('name', 'heart-outline')
      likeBtnCommentOff.setAttribute('name', 'heart-outline')
    }
    const likeCntComment = document.querySelector(`#comment-${commentPk}-likecnt`)
    const likeCntCommentOff = document.querySelector(`#comment-${commentPk}-likecnt-off`)
    likeCntComment.innerText = response.data.likeCount
    likeCntCommentOff.innerText = response.data.likeCount
  })

}