        <div class="col-sm-3 col-md-2 sidebar">
          <ul class="nav nav-sidebar">
            <li <?php if($menu=="main"){ echo "class='active'"; } ?>><a href="main.php"><span class="glyphicon glyphicon-home"></span> 首页</a></li>
            <li <?php if($menu=="stor"){ echo "class='active'"; } ?>><a href="stormgr.php"><span class="menu-tree-father-flag glyphicon glyphicon-chevron-<?php echo in_array($menu,array("stor","lv","vg","raid","disk"))?"down":"right"; ?>"></span> 存储管理</a>
                <ul class="nav accordion_list_child  <?php if(!in_array($menu,array("stor","lv","vg","raid","disk"))){ echo "hidden"; } ?>">
                    <li <?php if($menu=="lv"){ echo "class='active'"; } ?>><a href="lvmgr.php"><span class="glyphicon glyphicon-inbox"></span> 逻辑卷管理</a></li>
                    <li <?php if($menu=="vg"){ echo "class='active'"; } ?>><a href="vgmgr.php"><span class="glyphicon glyphicon-blackboard"></span> 存储池管理</a></li>
                    <li <?php if($menu=="raid"){ echo "class='active'"; } ?>><a href="raidmgr.php"><span class="glyphicon glyphicon-tasks"></span> RAID管理</a></li>
                    <li <?php if($menu=="disk"){ echo "class='active'"; } ?>><a href="diskmgr.php"><span class="glyphicon glyphicon-hdd"></span> 磁盘管理</a></li>
                </ul>
                <div class='menu-tree-father'></div>
            </li>
            <li <?php if($menu=="iscsi"){ echo "class='active'"; } ?>><a href="mapmgr.php"><span class="glyphicon glyphicon-transfer"></span> Target管理</a></li>
            <li <?php if($menu=="sys"){ echo "class='active'"; } ?>><a href="sysmgr.php"><span class="menu-tree-father-flag glyphicon glyphicon-chevron-<?php echo in_array($menu,array("sys","net","dt"))?"down":"right"; ?>"></span> 系统配置</a>
                <ul class="nav accordion_list_child  <?php if(!in_array($menu,array("sys","net","dt"))){ echo "hidden"; } ?>">
                    <li <?php if($menu=="net"){ echo "class='active'"; } ?>><a href="netmgr.php"><span class="glyphicon glyphicon-th"></span> 网络配置</a></li>
                    <li <?php if($menu=="dt"){ echo "class='active'"; } ?>><a href="dtmgr.php"><span class="glyphicon glyphicon-time"></span> 日期时间</a></li>
                </ul>
                <div class='menu-tree-father'></div>
            </li>
            <li <?php if($menu=="cluster"){ echo "class='active'"; } ?>><a href="clustermgr.php"><span class="glyphicon glyphicon-cog"></span> 集群配置</a></li>
          </ul>
        </div>