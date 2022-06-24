layui.use(['table', 'jquery'], function () {
    var table = layui.table;
    var $ = layui.jquery;
    var max_check_num = 10;
    var quanju = new Array();//全局
    var huancun = new Array();//缓存

    function show_user() {
        table.render({
        elem: '#test'
        , url: '/test_app_01/user.json/'
        , toolbar: '#toolbar_query_user' //开启头部工具栏，并为其绑定左侧模板
        , defaultToolbar: ['filter', 'exports', 'print', { //自定义头部工具栏右侧图标。如无需自定义，去除该参数即可
            title: '提示'
            , layEvent: 'LAYTABLE_TIPS'
            , icon: 'layui-icon-tips'
        }]
        , title: '用户数据表'
        , limit: 5
        , cols: [[
            {type: 'checkbox', fixed: 'left'},
            {field: 'id', width: 80, title: 'ID', sort: true}
            , {field: 'user_id', width: 80, title: '用户名'}
            , {field: 'vote_id', width: 80, title: '性别', sort: true}
            , {field: 'group_id', width: 80, title: '城市'}
            , {field: 'create_time', title: '时间', sort: true}
        ]]
        , page: true
        , done: function (res, curr, count) {
            //数据表格加载完成时调用此函数
            //如果是异步请求数据方式，res即为你接口返回的信息。
            //设置全部数据到全局变量
            quanju = res.data;

            //在缓存中找到id ,然后设置data表格中的选中状态
            //循环所有数据，找出对应关系，设置checkbox选中状态
            for (var i = 0; i < res.data.length; i++) {
                if (huancun.includes(res.data[i].id)) {
                    res.data[i]["LAY_CHECKED"] = 'true';
                    var index = res.data[i]['LAY_TABLE_INDEX'];
                    $('.layui-table tr[data-index=' + index + '] input[type="checkbox"]').prop('checked', true);
                    $('.layui-table tr[data-index=' + index + '] input[type="checkbox"]').next().addClass('layui-form-checked');
                }
            }
            //设置全选checkbox的选中状态，只有改变LAY_CHECKED的值， table.checkStatus才能抓取到选中的状态
            var checkStatus = table.checkStatus('test');//这里的studentTable是指分页中的id
            if (checkStatus.isAll) {//是否全选
                //layTableAllChoose
                $('.layui-table th[data-field="0"] input[type="checkbox"]').prop('checked', true);//data-field值默认为0，如果在分页部分自定义了属性名，则需要改成对应的属性名
                $('.layui-table th[data-field="0"] input[type="checkbox"]').next().addClass('layui-form-checked');//data-field值默认为0，如果在分页部分自定义了属性名，则需要改成对应的属性名
            }
        }
    });
    }

    //触发事件
    table.on('toolbar(test)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {
            case 'search':
                let select_value = $("#select_value_user").val();
                let select_data = $("#select_data_user").val();
                table.reload('test', {
                    url: '/test_app_01/user.json/'
                    , where: {
                        conditions: select_value + "=" + select_data
                    } //设定异步数据接口的额外参数
                    //,height: 300
                    , page: {
                        curr: 1 //重新从第 1 页开始
                    }
                });
                break;
        }
        ;
    });

    $('#agree_button').on('click', () => {
        var checkStatus = table.checkStatus("test");
        var data = checkStatus.data;
        if (huancun.length > 10) {
            layer.msg('你选中了：' + huancun.length + ' 个，超过最大可选数 ' + max_check_num + ' 个');
        } else if (data.length <= 0) {
            layer.msg('请选中需要封停的玩家');
        } else {
            var rname_arr = [], id_arr = [];
            data.forEach((k) => {
                rname_arr.push(k.user_id);
                id_arr.push(k.id);
            })
            $("#play_user").val(rname_arr.join(","))
            $("#play_user_id").val(id_arr.join("|"))
        }
    })
    $('#cancel_button').on('click', () => {
        huancun.length = 0
        layui.each(layui.table.cache["test"], function (i, item) {
            if (item.LAY_CHECKED) {
                $('.layui-form-checkbox.layui-form-checked', this.parent).click();
                // item.removeClass("layui-form-checked");
                // delete item.LAY_CHECKED;
                // item.LAY_CHECKED = true;
            }
        });
        $("#play_user").val("")
        $("#play_user_id").val("")
    })
    table.on('checkbox(test)', function (obj) {
        if (obj.checked == true) {
            if (obj.type == 'one') {
                huancun.push(obj.data.id);
            } else {
                for (var i = 0; i < quanju.length; i++) {
                    huancun.push(quanju[i].id);
                }
            }
        } else {
            if (obj.type == 'one') {
                for (var i = 0; i < huancun.length; i++) {
                    if (huancun[i] == obj.data.id) {
                        removeByValue(huancun, huancun[i]);//调用自定义的根据值移除函数
                    }
                }
            } else {
                for (var i = 0; i < huancun.length; i++) {
                    for (var j = 0; j < quanju.length; j++) {
                        if (huancun[i] == quanju[j].id) {
                            removeByValue(huancun, +huancun[i]);//调用自定义的根据值移除函数
                        }
                    }
                }
            }
        }
    });

    //自定义方法，根据值去移除
    function removeByValue(arr, val) {
        for (var i = 0; i < arr.length; i++) {
            if (arr[i] == val) {
                arr.splice(i, 1);
                break;
            }
        }
    }

    $('#demoReload').on('click', function () {
        show_user()
        layer.open({
            title: ["选择玩家（最大可选" + max_check_num + "个）", 'font-size:18px;'],
            type: 1, //类型
            anim: 4, //弹出方式
            skin: 'layui-layer-molv',
            area: ['600px', '450px'],
            content: $("#show_user_div"),
            shadeClose: true,
            shade: false,
            end: function (res) {
                $("#show_user_div").css("display", 'none');
            }
        })
    });
});
