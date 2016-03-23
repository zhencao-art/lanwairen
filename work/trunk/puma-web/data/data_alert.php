<?php    
    require_once "../include/puma-common.php";
    require_once "../include/data_util.php";
    
    $fun = @$_REQUEST["func"];
    
    if(function_exists($fun)){
        print $fun();
    }else{
        print "action not exist";
    }
    
    function alert_list(){
        $res = array("result"=>true);
        $htmls = "<tr>
                <td><span class='color_5'>紧急</span></td>
                <td>Problem</td>
                <td>2015-11-02 10:11:22</td>
                <td>Disk</td>
                <td>Disk错误</td>
            </tr>
            <tr>
                <td><span class='color_4'>重要</span></td>
                <td>Problem</td>
                <td>2015-11-02 10:16:22</td>
                <td>Disk</td>
                <td>Disk错误</td>
            </tr>
            <tr>
                <td><span class='color_4'>重要</span></td>
                <td>Problem</td>
                <td>2015-11-02 10:16:22</td>
                <td>Disk</td>
                <td>Disk错误</td>
            </tr>
            <tr>
                <td><span class='color_4'>重要</span></td>
                <td>Problem</td>
                <td>2015-11-02 10:18:22</td>
                <td>Disk</td>
                <td>Disk错误</td>
            </tr>
            <tr>
                <td><span class='color_4'>重要</span></td>
                <td>Problem</td>
                <td>2015-11-02 10:26:22</td>
                <td>Disk</td>
                <td>Disk错误</td>
            </tr>";
        $res["page_count"] = 300;
        $res["data"] = $htmls;
        return json_encode($res);
    }
    
    function event_list(){
        $res = array("result"=>true);
        $htmls = "<tr>
                <td>2015-11-02 10:11:22</td>
                <td>admin</td>
                <td>卷vol_test</td>
                <td>新增卷vol_test</td>
                <td><span class='color_green'>成功</span></td>
            </tr>
            <tr>
                <td>2015-11-02 10:11:22</td>
                <td>admin</td>
                <td>卷vol_test</td>
                <td>新增卷vol_test1</td>
                <td><span class='color_green'>成功</span></td>
            </tr>
            <tr>
                <td>2015-11-02 10:11:22</td>
                <td>admin</td>
                <td>卷vol_test</td>
                <td>新增卷vol_test2</td>
                <td><span class='color_green'>成功</span></td>
            </tr>
            <tr>
                <td>2015-11-02 10:11:22</td>
                <td>admin</td>
                <td>卷vol_test</td>
                <td>新增卷vol_test3</td>
                <td><span class='color_green'>成功</span></td>
            </tr>
            <tr>
                <td>2015-11-02 10:11:22</td>
                <td>admin</td>
                <td>卷vol_test</td>
                <td>删除卷vol_test4</td>
                <td><span class='color_green'>成功</span></td>
            </tr>";
        $res["page_count"] = 100;
        $res["data"] = $htmls;
        return json_encode($res);
    }
?>