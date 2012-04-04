/**
 * Created with PyCharm.
 * User: rauch
 * Date: 04.04.12
 * Time: 14:38
 * To change this template use File | Settings | File Templates.
 */

function customMenu(node) {
    // The default set of all items
    var items = {
        downloadItem:{ // The "rename" menu item
            label:"Download",
            action:function () {
                downloadItem(node)
            }
        },
        uploadItem:{ // The "rename" menu item
            label:"Upload",
            action:function () {
                alert("Upload")
            }
        },
        renameItem:{ // The "rename" menu item
            label:"Rename",
            action:function () {
                this.rename(node);
            }
        },
        deleteItem:{ // The "delete" menu item
            label:"Delete",
            action:function () {
                alert("Delete")
            }
        }
    };

    if ($(node).attr("rel") == "folder") {
        // Delete the "delete" menu item
        delete items.deleteItem;
        delete items.downloadItem;
    }
    if ($(node).attr("rel") == "file") {
        // Delete the "delete" menu item
        delete items.uploadItem;
    }

    return items;
}

function removeItem(node) {

    var itemToRemove = node;

    data = {
        selectedItemFullName:itemToRemove["id"]
    };
    new Ajax.Request("/webtorque/ajax", {
        method:'post',
        parameters:data,
        onSuccess:function (transport) {
            var data = transport.responseJSON;

            if (data["success"] == true) {
                fileSystemTree.deleteNode(nodeId)
            }
            else if (data["success"] == false) {
                alert("This item couldn't be removed!\r\n" + data["errorMessage"])
            }
        },
        onFailure:function () {
            alert("This item couldn't be removed!\r\n")
        },
        onComplete:function () {

        }
    });
}

function createItem(nodeId) {

    var itemToAdd = fileSystemTree.getNodeById(nodeId);

    var formToUpload = $("formToUpload");

    $("currentDirectoryInput").value = itemToAdd["fullName"];

    formToUpload.submit()
}

function downloadItem(node) {

    var itemToDownload = node;

    var formToDownload = $("#formToDownload");

    $("#currentFileInput").val(itemToDownload.attr("id"));

    formToDownload.submit()
}


function createItemDir() {

    var isDirectoryCb = $("isDirectoryCb");
    if (isDirectoryCb["value"]) {
        $("directoryForm").submit()
    } else {
        $("fileForm").submit()
    }
}

function changeFileType() {

    var isDirectoryCb = $("isDirectoryCb");
    if (isDirectoryCb["checked"]) {
        $("mySubmit").setStyle({display:"block"})
        $("djangoSubmit").setStyle({display:"none"})
        $("directoryName").disabled = false;
    } else {
        $("mySubmit").setStyle({display:"none"})
        $("djangoSubmit").setStyle({display:"block"})
        $("directoryName").disabled = "disabled";
    }

}


