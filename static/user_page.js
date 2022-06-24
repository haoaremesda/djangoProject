layui.use('table', function () {
    var table = layui.table;
    var max_check_num = 10;

    table.render({
        elem: '#test'
        , url: '/test_app_01/user.json'
        , where: {token: 'sasasas', id: 123}
        , toolbar: "#toolbarDemo"
        , cols: [[
            {type: 'checkbox', fixed: 'left'},
            {field: 'id', width: 80, title: 'ID', sort: true}
            , {field: 'user_id', width: 80, title: '用户名'}
            , {field: 'vote_id', width: 80, title: '性别', sort: true}
            , {field: 'group_id', width: 80, title: '城市'}
            , {field: 'create_time', title: '积分', sort: true}
        ]]
        , page: true
        // , id: 'testReloadx'
    });
     //头工具栏事件
    table.on('toolbar(test)', function (obj) {
        var checkStatus = table.checkStatus(obj.config.id);
        switch (obj.event) {
            case 'getCheckData':
                var data = checkStatus.data;
                layer.alert(JSON.stringify(data));
                break;
            case 'getCheckLength':
                var data = checkStatus.data;
                layer.msg('选中了：' + data.length + ' 个');
                break;
            case 'isAll':
                layer.msg(checkStatus.isAll ? '全选' : '未全选');
                break;

            //自定义头工具栏右侧图标 - 提示
            case 'LAYTABLE_TIPS':
                layer.alert('这是工具栏右侧自定义的一个图标按钮');
                break;
        }
        ;
    });
    var $ = layui.$, active = {
        reload: function () {
            var demoReload = $('#demoReload');

            //执行重载
            table.reload('testReloadx', {
                page: {
                    curr: 1 //重新从第 1 页开始
                }
                , where: {
                    id: demoReload.val()
                }
            });
        }
    };

    $('.demoTable .layui-btn').on('click', function () {
        var type = $(this).data('type');
        active[type] ? active[type].call(this) : '';
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
    $('#agree_button').on('click', () => {
        var checkStatus = table.checkStatus("test");
        var data = checkStatus.data;
        if (data.length > 10) {
            layer.msg('你选中了：' + data.length + ' 个，超过最大可选数 ' + max_check_num + ' 个');
        } else if (data.length <= 0) {
            layer.msg('请选中需要封停的玩家');
        } else {
            var rname_arr = [], id_arr = [];
            data.forEach((k) => {
                rname_arr.push(k.rname);
                id_arr.push(k.id);
            })
            $("#play_user").val(rname_arr.join(","))
            $("#play_user_id").val(id_arr.join("|"))
        }
    })
});