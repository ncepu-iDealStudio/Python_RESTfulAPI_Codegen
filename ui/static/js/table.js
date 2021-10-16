window.onload = function () {
    // 数据处理，转jison
    for (let item in data) {
        data[item] = data[item].replace(/&#39;/g, "'");
        data[item] = eval("(" + data[item] + ")")
    }
    document.getElementById(data[0].table).click();
}

currentTable = ""

function businessKey() {
    let keyDiv = document.getElementById("businessKeyRule");
    if (document.getElementById("isBusinessKey").checked == true) {

        keyDiv.style.display = 'block';
    } else {
        keyDiv.style.display = 'none';
    }
}

function toTableInfo() {

    let tablename = document.getElementById("tableName");
    let isDeleted = document.getElementById("isDeleted");
    let filed = document.getElementById("filed");
    let isBusinessKey = document.getElementById("isBusinessKey");
    let textRule = document.getElementById("textRule");
    let selectBusinessKey = document.getElementById("selectBusinessKey");
    for (let item in data) {
        if (data[item].table == event.target.id) {
            for (let filed in data[item]['filed']) {
                if (data[item]['filed'][filed] == "IsDelete") {
                    document.getElementById("isDeleted").disabled = false;
                    document.getElementById("isDeleted").style = "cursor: auto;";
                    break;
                } else {
                    document.getElementById("isDeleted").disabled = true;
                    document.getElementById("isDeleted").style = "cursor: not-allowed;";
                }
            }
            currentTable = data[item].table;
            tablename.innerText = data[item].table;
            isDeleted.checked = data[item].isdeleted;
            if (data[item].isbusinesskey != "") {
                isBusinessKey.checked = true;
            } else {
                isBusinessKey.checked = false;
            }

            businessKey();

            // 删除所有子节点
            filed.innerHTML = "";
            selectBusinessKey.innerHTML = "";
            // 加载加密字段  业务主键自段
            for (let i in data[item].filed) {
                let li = document.createElement("li");
                let a = document.createElement("a");
                let label = document.createElement("label");
                let input = document.createElement("input");
                let text = document.createElement("text");
                let option = document.createElement("option");
                let filedname = data[item].filed[i].field_name;
                input.type = "checkbox";
                for (let i = 0; i < data[item].encrypt.length; i++) {
                    if (data[item].encrypt[i] == filedname) {
                        input.checked = true;
                        break;
                    }
                }

                text.innerText = filedname;
                option.innerText = filedname;
                selectBusinessKey.appendChild(option)
                filed.appendChild(li);
                li.appendChild(a);
                a.appendChild(label)
                label.appendChild(input);
                label.appendChild(text);
                if (data[item].filed[i].field_type != 'str') {
                    input.disabled = true;
                    input.style = "cursor: not-allowed;";
                }
            }
            if (data[item].isbusinesskey != "") {
                selectBusinessKey.value = data[item].isbusinesskey;
            }
            selectBusinessKeyRule();
            textRule.value = data[item].businesskeyrule;
        }
    }
    let animation = document.getElementById('btn-save');
    animation.style.animationDuration = "0s";

}

function selectBusinessKeyRule() {
    let selectBusinessKey = document.getElementById("selectBusinessKey");
    let tablename = document.getElementById("tableName");
    let textRule = document.getElementById("textRule");
    for (let item in data) {
        if (data[item].table == tablename.innerText) {
            for (let i in data[item].filed) {
                if (data[item].filed[i].field_name == selectBusinessKey.options[selectBusinessKey.selectedIndex].value) {
                    textRule.innerHTML = '';
                    if (data[item].filed[i].field_type == 'int') {
                        let option_create_random_id = document.createElement("option");
                        textRule.appendChild(option_create_random_id);
                        option_create_random_id.innerText = "create_random_id";
                        textRule.appendChild(option_create_random_id);
                    } else if (data[item].filed[i].field_type == 'str') {
                        let option_create_random_id = document.createElement("option");
                        textRule.appendChild(option_create_random_id);
                        option_create_random_id.innerText = "create_random_id";
                        textRule.appendChild(option_create_random_id);

                        let create_hashlib_id = document.createElement("option");
                        textRule.appendChild(create_hashlib_id);
                        create_hashlib_id.innerText = "create_hashlib_id";
                        textRule.appendChild(create_hashlib_id);

                        let create_uid = document.createElement("option");
                        textRule.appendChild(create_uid);
                        create_uid.innerText = "create_uid";
                        textRule.appendChild(create_uid);
                    }
                }
            }
        }
    }
}

function saveTableInfo() {
    let isDeleted = document.getElementById("isDeleted");
    let filed = document.getElementById("filed");
    let isBusinessKey = document.getElementById("isBusinessKey")
    let selectBusinessKey = document.getElementById("selectBusinessKey")
    let textRule = document.getElementById("textRule");
    for (let item in data) {
        if (data[item].table == currentTable) {
            data[item].issave = 'true';
            let table = document.getElementById(currentTable);
            let tablechilds = table.childNodes;
            tablechilds[1].style.color = "#0F9D24";
            if (isDeleted.checked) {
                data[item].isdeleted = 'true';
            } else {
                data[item].isdeleted = '';
            }
            if (isBusinessKey.checked) {
                data[item].isbusinesskey = selectBusinessKey.options[selectBusinessKey.selectedIndex].value;
            }
            data[item].businesskeyrule = textRule.value;
            // 保存加密字段
            data[item].encrypt = [];
            let filedchilds = filed.childNodes;
            for (let i = 0; i < filedchilds.length; i++) {
                let filedcheck = filedchilds[i].firstChild.firstChild.firstChild;
                if (filedcheck.checked == true) {
                    let filedname = filedcheck.nextSibling.innerText;
                    data[item].encrypt.push(filedname);
                }
            }
            break;
        }
    }
    let animation = document.getElementById('btn-save');
    animation.style.animationDuration = "2s";
    animation.addEventListener("animationend", nextAnimation);
    animation.className = "alert alert-success alert-show";

}

function nextAnimation() {
    document.getElementById('btn-save').className = "alert alert-success alert-save";
}

function removeTableInfo() {
    let msg = "清空后该表信息将不再被写入配置";
    if (confirm(msg)) {
        for (let item in data) {
            if (data[item].table == currentTable) {
                data[item].issave = '';
                let table = document.getElementById(currentTable);
                let tablechilds = table.childNodes;
                tablechilds[1].style.color = "#A7A7A7";
                data[item].isdeleted = "";
                data[item].encrypt = [];
                data[item].isbusinesskey = "";
                data[item].businesskeyrule = "";
                table.click();
                break;
            }
        }
        let animation = document.getElementById('btn-save');
        animation.style.animationDuration = "0s";
    }
}

function sendData() {
    let isalert = true;
    for (let item in data) {
        if (data[item].issave)
            isalert = false;
    }
    if (isalert) {
        let msg = "你未配置任何一张数据库表!!!\n请确认是否续";
        if (confirm(msg)) {
            let jsonData = JSON.stringify(data);
            window.location.href = "/tableinfo/" + jsonData;
        }
    } else {
        let jsonData = JSON.stringify(data);
        window.location.href = "/tableinfo/" + jsonData;
    }
}

function setActive() {
    let active = document.getElementsByClassName("active");
    for (let item in active) {
        active[item].className = "";
    }
    let evt = event.target.parentNode;
    evt.className = "active";
}