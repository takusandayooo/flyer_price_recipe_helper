//アクセス権限参考:https://qiita.com/kou1121/items/274e30dcc0d4b67d04d1
//APIの本体
function doGet(e) {

    const p = e.parameter;
    const file = zippress(p.fileID);
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
    const fileName = file.getName();
    const fileURL = file.getUrl();
    const fileID = file.getId();
    var body;
    body = {
        text: { "Name": fileName, "URL": fileURL, "ID": fileID }
    };


    // レスポンスの作成
    const response = ContentService.createTextOutput();
    // Mime TypeをJSONに設定
    response.setMimeType(ContentService.MimeType.JSON);
    // JSONテキストをセットする
    response.setContent(JSON.stringify(body));

    return response;
}
//zipファイルを生成し、そのダウンロードURLを追加
function zippress(zipfolder) {
    //圧縮するファイルが入ってるフォルダを指定
    const folder = DriveApp.getFolderById(zipfolder);
    try {
        folder.getFoldersByName("ZipFolder").next().setTrashed(true);
    } catch {
        ;
    }
    Utilities.sleep(10);
    const zipman = Utilities.zip(getBlobs(folder, ''), 'photo.zip');

    const zip_folder = folder.createFolder("ZipFolder");
    return zip_folder.createFile(zipman);

}
function getBlobs(rootFolder, path) {
    var blobs = [];
    const files = rootFolder.getFiles();
    while (files.hasNext()) {
        var file = files.next().getBlob();
        file.setName(path + file.getName());
        blobs.push(file);
    }
    const folders = rootFolder.getFolders();
    while (folders.hasNext()) {
        var folder = folders.next();
        var fPath = path + folder.getName() + '/';
        blobs.push(Utilities.newBlob([]).setName(fPath));
        blobs = blobs.concat(getBlobs(folder, fPath));
    }
    return blobs;
}