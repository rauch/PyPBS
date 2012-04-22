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
        downloadItem:{ // The "download" menu item
            label:"Download",
            action:function () {
                downloadItem(node)
            }
        },
        uploadItem:{ // The "upload" menu item
            label:"Upload",
            action:function () {
                createItem(node);
            }
        },
//        renameItem:{ // The "rename" menu item
//            label:"Rename",
//            action:function () {
//                this.rename(node);
//            }
//        },
        deleteItem:{ // The "delete" menu item
            label:"Delete",
            action:function () {
                removeItem(node);
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

function downloadItem(node) {
    var itemToDownload = node;
    var formToDownload = $("#formToDownload");
    $("#currentFileInput").val(itemToDownload.attr("id"));

    formToDownload.submit()
}

function createItem(node) {
    var formToUpload = $("#formToUpload");
    $("#currentDirectoryInput").val(node.attr("id"));

    formToUpload.submit()
}

function showInfo(text) {
    $(".info").fadeIn("fast", function () {
        $(".info").html(text);
        setTimeout(function () {
            $('.info').fadeOut(3000);
        }, 4000);
    });
}

function showSuccess(text) {
    $(".success").fadeIn("fast", function () {
        $(".success").html(text);
        setTimeout(function () {
            $('.success').fadeOut(3000);
        }, 4000);
    });
}

function showWarning(text) {
    $(".warning").fadeIn("fast", function () {
        $(".warning").html(text);
        setTimeout(function () {
            $('.warning').fadeOut(3000);
        }, 4000);
    });
}

function showError(text) {
    $(".error").fadeIn("fast", function () {
        $(".error").html(text);
        setTimeout(function () {
            $('.error').fadeOut(3000);
        }, 4000);
    });
}

