function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    sheet.appendRow([
      new Date(),
      data.studentId,
      data.name,
      data.type,
      data.level,
      data.score,
      data.total,
      Math.round(data.score / data.total * 100) + '%'
    ]);
  } catch (e) {
    // 오류가 발생해도 클라이언트에 영향 없음
  }
  return ContentService.createTextOutput('ok');
}
