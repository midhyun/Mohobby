const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const requestUserId = document.querySelector('#request-user-id').value
dayjs.extend(window.dayjs_plugin_relativeTime)
dayjs.extend(window.dayjs_plugin_utc)
dayjs.extend(window.dayjs_plugin_timezone)
dayjs.locale('ko')
console.log(dayjs.tz(new Date()))
console.log(dayjs.tz.guess())
const commentInput = document.querySelector('#commentinput')
const commentCount = document.querySelector('#comment-count')
// 댓글생성 폼
const commentForm = document.querySelector(`#comment-form`)
// 댓글 리스트
const commentList = document.querySelector('#comment-list')
// 댓글 리스트 - 오프캔버스
const commentListOff = document.querySelector('#comment-list-off')
// 댓글 생성 함수
function submitComment(event) {
    event.preventDefault();
    const pk = event.target.dataset.hobbyId;

    axios({
        method: 'post',
        url: `/hobby/${pk}/comment_create`,
        headers: { 'X-CSRFToken': csrftoken},
        data: new FormData(commentForm)
    })
    .then(response => {
      // detail 페이지 댓글 제한 7개
        commentList.textContent = ""
        for (let i=0; i < response.data.comments_data.length; i++){
            let isLike = ""
            if (i == 7){
              break;
            }
            if (response.data.comments_data[i].is_like === true) {
              isLike = "heart"
            } else {
              isLike = "heart-outline"
            }
            commentList.insertAdjacentHTML('beforeend', `<hr>
            <div class="d-flex justify-content-between">
            <div class="comment-elem" >
                <img class="comment-image" src="${ response.data.comments_data[i].image }" alt="">
              <div>
                <p>${ response.data.comments_data[i].user }</p>
                <p>${ response.data.comments_data[i].content }</p>
                <div>
                  <p class="text-muted" style="font-size:12px"><span>${dayjs.utc(response.data.comments_data[i].created_at).local().fromNow()}</span> <span>좋아요 <span id="comment-${response.data.comments_data[i].pk}-likecnt">${response.data.comments_data[i].likeCount}</span>개</span> <span>답글달기</span> 
                  <ion-icon onclick="getDeleteComment(this)" type="button" data-bs-toggle="modal" data-bs-target="#comment-delete" data-comment-id="${response.data.comments_data[i].pk}" data-user="${ response.data.comments_data[i].user }" name="ellipsis-horizontal"></ion-icon>
                  </p>
                </div>
              </div>
            </div>
            <div>
            <ion-icon data-action="like" id="comment-${response.data.comments_data[i].pk}-likebtn" class="comment-like-btn" data-comment-id="${response.data.comments_data[i].pk}" style="color:#E84545" name=${isLike}></ion-icon>
            </div>
            </div>`
            )}
        commentInput.value = ""
        commentCount.innerText = response.data.comments_data.length 

        
        // 오프캔버스 더보기로 모든 댓글 구현
        commentListOff.textContent = ""
        for (let i=0; i < response.data.comments_data.length; i++){
            let isLike = ""
            if (response.data.comments_data[i].is_like === true) {
              isLike = "heart"
            } else {
              isLike = "heart-outline"
            }
            commentListOff.insertAdjacentHTML('beforeend', `<hr>
            <div class="d-flex justify-content-between">
            <div class="comment-elem" >
                <img class="comment-image" src="${ response.data.comments_data[i].image }" alt="">
              <div>
                <p>${ response.data.comments_data[i].user }</p>
                <p>${ response.data.comments_data[i].content }</p>
                <div>
                  <p class="text-muted" style="font-size:12px"><span>${dayjs.utc(response.data.comments_data[i].created_at).local().fromNow()}</span> <span>좋아요 <span id="comment-${response.data.comments_data[i].pk}-likecnt-off">${response.data.comments_data[i].likeCount}</span>개</span> <span>답글달기</span> 
                  <ion-icon onclick="getDeleteComment(this)" type="button" data-bs-toggle="modal" data-bs-target="#comment-delete" data-comment-id="${response.data.comments_data[i].pk}" data-user="${ response.data.comments_data[i].user_pk }" name="ellipsis-horizontal"></ion-icon>
                  </p>
                </div>
              </div>
            </div>
            <div>
              <ion-icon data-action="like" id="comment-${response.data.comments_data[i].pk}-likebtn-off" class="comment-like-btn" data-comment-id="${response.data.comments_data[i].pk}" style="color:#E84545" name=${isLike}></ion-icon>
            </div>
            </div>`
            )}

    })

};



const likeBtn = document.querySelector('.hobby-like-btn');
function likeHobby(e) {
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
};

function likeComment(e) {
  const commentPk = e.target.dataset.commentId;
  const likeBtnComment = document.querySelector(`#comment-${commentPk}-likebtn`);
  const likeBtnCommentOff = document.querySelector(`#comment-${commentPk}-likebtn-off`);
  if (e.target.dataset.action == 'like'){
    axios({
      method: 'get',
      url: `/hobby/${commentPk}/like_comment`,
    })
    .then(response => {
      console.log(response.data)
      if (response.data.is_like === true ) {
        try { likeBtnComment.setAttribute('name', 'heart') } catch(error) {};
        likeBtnCommentOff.setAttribute('name', 'heart')
      } else {
        try { likeBtnComment.setAttribute('name', 'heart-outline') } catch(error) {};
        likeBtnCommentOff.setAttribute('name', 'heart-outline')
      };
      try {
        const likeCntComment = document.querySelector(`#comment-${commentPk}-likecnt`)
        likeCntComment.innerText = response.data.likeCount
      } catch(error) {};
      const likeCntCommentOff = document.querySelector(`#comment-${commentPk}-likecnt-off`)
      likeCntCommentOff.innerText = response.data.likeCount
    })
  
  };
  };


function getDeleteComment(e) {
  console.log(e.target.dataset.user)
  console.log(requestUserId)
  if (e.target.dataset.action == 'getDelete') {
    const btnDiv = document.querySelector('.modal-body')
    if (requestUserId === e.target.dataset.user) {
      btnDiv.innerHTML = `<button onclick="deleteComment(this)" data-bs-dismiss="modal" data-comment-id="${e.target.dataset.commentId}" id="comment-delete-btn" class="mt-3 submit_btn slide_button" type="button">댓글 삭제하기</button>`
    } else {
      btnDiv.innerHTML = `<button id="comment-report-btn" data-bs-dismiss="modal" class="mt-3 submit_btn slide_button" type="button">댓글 신고하기</button>`
    }};
};

function deleteComment(e) {
  const comment_pk = e.dataset.commentId;
  console.log(comment_pk)

  axios({
      method: 'post',
      url: `/hobby/${comment_pk}/comment_delete`,
      headers: { 'X-CSRFToken': csrftoken},
  })
  .then(response => {
    // detail 페이지 댓글 제한 7개
      commentList.textContent = ""
      for (let i=0; i < response.data.comments_data.length; i++){
          let isLike = ""
          if (i == 7){
            break;
          }
          if (response.data.comments_data[i].is_like === true) {
            isLike = "heart"
          } else {
            isLike = "heart-outline"
          }
          commentList.insertAdjacentHTML('beforeend', `<hr>
          <div class="d-flex justify-content-between">
          <div class="comment-elem" >
              <img class="comment-image" src="${ response.data.comments_data[i].image }" alt="">
            <div>
              <p>${ response.data.comments_data[i].user }</p>
              <p>${ response.data.comments_data[i].content }</p>
              <div>
                <p class="text-muted" style="font-size:12px"><span>${dayjs.utc(response.data.comments_data[i].created_at).local().fromNow()}</span> <span>좋아요 <span id="comment-${response.data.comments_data[i].pk}-likecnt">${response.data.comments_data[i].likeCount}</span>개</span> <span>답글달기</span> 
                <ion-icon data-action="getDelete" type="button" data-bs-toggle="modal" data-bs-target="#comment-delete" data-comment-id="${response.data.comments_data[i].pk}" data-user="${ response.data.comments_data[i].user_pk }" name="ellipsis-horizontal"></ion-icon>
                </p>
              </div>
            </div>
          </div>
          <div>
            <ion-icon data-action="like" id="comment-${response.data.comments_data[i].pk}-likebtn" class="comment-like-btn" data-comment-id="${response.data.comments_data[i].pk}" style="color:#E84545" name=${isLike}></ion-icon>
          </div>
          </div>`
          )}
      commentInput.value = ""
      commentCount.innerText = response.data.comments_data.length 
      // 오프캔버스 더보기로 모든 댓글 구현
      commentListOff.textContent = ""
      for (let i=0; i < response.data.comments_data.length; i++){
          let isLike = ""
          if (response.data.comments_data[i].is_like === true) {
            isLike = "heart"
          } else {
            isLike = "heart-outline"
          }
          commentListOff.insertAdjacentHTML('beforeend', `<hr>
          <div class="d-flex justify-content-between">
          <div class="comment-elem" >
              <img class="comment-image" src="${ response.data.comments_data[i].image }" alt="">
            <div>
              <p>${ response.data.comments_data[i].user }</p>
              <p>${ response.data.comments_data[i].content }</p>
              <div>
                <p class="text-muted" style="font-size:12px"><span>${dayjs.utc(response.data.comments_data[i].created_at).local().fromNow()}</span> <span>좋아요 <span id="comment-${response.data.comments_data[i].pk}-likecnt-off">${response.data.comments_data[i].likeCount}</span>개</span> <span>답글달기</span> 
                <ion-icon data-action="getDelete" type="button" data-bs-toggle="modal" data-bs-target="#comment-delete" data-comment-id="${response.data.comments_data[i].pk}" data-user="${ response.data.comments_data[i].user_pk }" name="ellipsis-horizontal"></ion-icon>
                </p>
              </div>
            </div>
          </div>
          <div>
            <ion-icon data-action="like" id="comment-${response.data.comments_data[i].pk}-likebtn-off" class="comment-like-btn" data-comment-id="${response.data.comments_data[i].pk}" style="color:#E84545" name=${isLike}></ion-icon>
          </div>
          </div>`
          )};
  })
};

// 폼에 이벤트 추가
commentForm.addEventListener('submit', submitComment)
// 하트 아이콘 좋아요 이벤트 추가
commentList.addEventListener('click', likeComment)
// ... 아이콘 삭제모달 이벤트 추가
commentList.addEventListener('click', getDeleteComment)
// 오프캔버스에도 이벤트 추가
commentListOff.addEventListener('click', likeComment)
commentListOff.addEventListener('click', getDeleteComment)