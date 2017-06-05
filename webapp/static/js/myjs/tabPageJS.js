/**
 * Created by wangyu on 2017/3/20.
 */
function heredoc(fn) {
    return fn.toString().split('\n').slice(1, -1).join('\n') + '\n'
}

function showFirst() {
    $('#tabPage').empty();
    $('#showFirst').css('display','block');
}

function waike() {
    $('#showFirst').css('display','none');
    var addTemp = heredoc(function () {/*
     <div class="list-group">
     <a href="#" class="list-group-item active">
     外科手术分类
     </a>
     <a href="/index/puwai" class="list-group-item">普外科</a>
     <a href="/index/shenjing" class="list-group-item">神经外科</a>
     <a href="/index/guke" class="list-group-item">骨科</a>
     <a href="/index/miniao" class="list-group-item">泌尿外科</a>
     <a href="/index/xiongxin" class="list-group-item">胸心外科</a>
     <a href="/index/shaoshangAndzhengxing" class="list-group-item">烧伤和整形外科</a>
     </div
     */
    });

    $('#tabPage').empty(); //先清空后添加
    $('#tabPage').append(addTemp);
}

function fuchanke() {
    $('#showFirst').css('display','none');
    var addTemp = heredoc(function () {/*
     <div class="list-group">
     <a href="#" class="list-group-item active">
     妇产科手术分类
     </a>
     <a href="/index/fuke" class="list-group-item">妇科</a>
     <a href="/index/chanke" class="list-group-item">产科</a>
     </div
     */
    });

    $('#tabPage').empty();
    $('#tabPage').append(addTemp);
}

function yanke() {
    $('#showFirst').css('display','none');
    var addTemp = heredoc(function () {/*
     <div class="list-group">
     <a href="#" class="list-group-item active">
     眼科手术分类
     </a>
     <a href="/index/yanke_cut" class="list-group-item">切除类</a>
     <a href="/index/yanke_other" class="list-group-item">其他</a>
     </div
     */
    });

    $('#tabPage').empty();
    $('#tabPage').append(addTemp);
}

function erbihouke() {
    $('#showFirst').css('display','none');
    var addTemp = heredoc(function () {/*
     <div class="list-group">
     <a href="#" class="list-group-item active">
     耳鼻喉科手术分类
     </a>
     <a href="/index/ear" class="list-group-item">耳部手术</a>
     <a href="/index/nose" class="list-group-item">鼻部手术</a>
     <a href="/index/throat" class="list-group-item">喉部手术</a>
     </div
     */
    });

    $('#tabPage').empty();
    $('#tabPage').append(addTemp);
}

function kouqiangke() {
    $('#showFirst').css('display','none');
    var addTemp = heredoc(function () {/*
     <div class="list-group">
     <a href="#" class="list-group-item active">
     口腔喉科手术分类
     </a>
     <a href="/index/kouqiang" class="list-group-item">口腔科</a>
     </div
     */
    });

    $('#tabPage').empty();
    $('#tabPage').append(addTemp);
}

function toCummunityClick() {
    window.open('communityMain');
}

function searchOnclick() {
    $('#showFirst').css('display','none');
    var searchStr = $('#search_input').val();

    if (searchStr) {
        $.getJSON(
            $SCRIPT_ROOT +'/search',{
            tosearch: searchStr},
            function(data){
                $('#tabPage').empty();
                console.log(data);
                opera_name=data.operation_name;
                opera_explain=data.operation_explain;
                oper_todo=data.operation_after;
                oper_west=data.operation_west;
                opera_cina=data.operation_china;

                var addTemp = heredoc(function (){/*
                  <div class="panel panel-info">
                    <h3 id=oper_title></h3>
                    <h5 style="color:#5bc0de">手术介绍</h5>
                    <p id=oper_explain></p>
                    <h5 style="color:#5bc0de">术后处理</h5>
                    <p id=oper_todo></p>
                    <h5 style="color:#5bc0de">西医治疗</h5>
                    <p id=oper_west></p>
                    <h5 style="color:#5bc0de">中医处理</h5>
                    <p id=oper_china></p>
                  </div

                    */
                });
                $('#tabPage').append(addTemp);
                $('#oper_title').append(opera_name);
                $('#oper_explain').append(opera_explain);
                $('#oper_todo').append(oper_todo);
                $('#oper_west').append(oper_west);
                $('#oper_china').append(opera_cina);

            });
        }
        }

            // type: 'GET',
            // dataType: 'json', //希望服务器返回的数据格式
            // success: function(data) { //# 这里的data就是json格式的数据,data为返回数据
            //     console.log('chenggong');
            //     print(data);
            //     $('#tabPage').empty();
            //     var addTemp = heredoc(function () {/*
            //     <ul class="nav nav-tabs" role="tablist">
  //   <li role="presentation" class="active"><a href="#home" aria-controls="home" role="tab" data-toggle="tab">手术介绍</a></li>
  //   <li role="presentation"><a href="#profile" aria-controls="profile" role="tab" data-toggle="tab">术后处理</a></li>
  //   <li role="presentation"><a href="#messages" aria-controls="messages" role="tab" data-toggle="tab">西医治疗</a></li>
  //   <li role="presentation"><a href="#settings" aria-controls="settings" role="tab" data-toggle="tab">中医康复</a></li>
  // </ul>
  //
  // <div class="tab-content">
  //   <div role="tabpanel" class="tab-pane active" id="home">2131231</div>
  //   <div role="tabpanel" class="tab-pane" id="profile">1231231</div>
  //   <div role="tabpanel" class="tab-pane" id="messages">1231231</div>
  //   <div role="tabpanel" class="tab-pane" id="settings">12313</div>
  // </div>
            //      */
            //     })
            //     },
        //     error:function(error) {
        //         console.log('qqqq')
        //         console.log(error);
        //         alert('返回失败')
        //     }
        //
        // });



