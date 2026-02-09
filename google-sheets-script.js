/**
 * Скрипт для Google Таблицы — принимает данные от бота через Web App.
 * Инструкция:
 * 1. Создайте новую Google Таблицу (sheets.google.com)
 * 2. Расширения → Apps Script
 * 3. Удалите весь код и вставьте этот скрипт
 * 4. Сохраните (Ctrl+S)
 * 5. Развернуть → Новое развертывание → Тип: Веб-приложение
 *    - Выполнять от имени: Меня
 *    - Доступ: Все пользователи
 * 6. Нажмите «Развернуть», скопируйте URL
 * 7. В .env бота добавьте: SHEETS_WEBAPP_URL=скопированный_url
 */

function doGet(e) {
  // Handle GET requests (for testing/debugging)
  return ContentService.createTextOutput(JSON.stringify({
    ok: true,
    message: "Web App is working. Use POST requests to send data.",
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

function doPost(e) {
  try {
    // Log everything we receive for debugging
    Logger.log("=== doPost called ===");
    Logger.log("e exists: " + (e ? "yes" : "no"));
    
    // Check if function is called manually (for testing) vs via HTTP POST
    if (!e) {
      Logger.log("WARNING: doPost called without parameter. This might be a manual test.");
      Logger.log("To test properly, use the Web App URL with a POST request, not the function directly.");
      return _jsonResponse({ ok: false, error: "No request data. Use Web App URL for POST requests." }, 400);
    }
    
    Logger.log("e.postData exists: " + (e.postData ? "yes" : "no"));
    Logger.log("e.postData.contents exists: " + (e.postData && e.postData.contents ? "yes" : "no"));
    
    // Try to get data from different possible locations
    var postDataContents = null;
    if (e.postData && e.postData.contents) {
      postDataContents = e.postData.contents;
    } else if (e.parameter && e.parameter.data) {
      // Sometimes data comes as parameter
      postDataContents = e.parameter.data;
    } else if (e.postData && e.postData.getDataAsString) {
      // Try getDataAsString method
      postDataContents = e.postData.getDataAsString();
    }
    
    if (postDataContents) {
      Logger.log("postData.contents type: " + typeof postDataContents);
      Logger.log("postData.contents length: " + (postDataContents ? postDataContents.length : 0));
      Logger.log("postData.contents preview: " + (postDataContents ? String(postDataContents).substring(0, 200) : "null"));
    }
    
    // Try to parse JSON
    var json = null;
    if (postDataContents) {
      try {
        json = JSON.parse(postDataContents);
        Logger.log("JSON parsed successfully");
      } catch(parseErr) {
        Logger.log("JSON parse error: " + parseErr);
        // Try alternative parsing methods
        try {
          var contentsStr = String(postDataContents);
          json = JSON.parse(contentsStr);
          Logger.log("JSON parsed from string successfully");
        } catch(parseErr2) {
          Logger.log("JSON parse error from string: " + parseErr2);
        }
      }
    }
    
    if (!json) {
      Logger.log("Error: No data received or could not parse JSON");
      Logger.log("Full e object keys: " + (e ? Object.keys(e).join(", ") : "null"));
      if (e.postData) {
        Logger.log("e.postData keys: " + Object.keys(e.postData).join(", "));
      }
      return _jsonResponse({ ok: false, error: "No data" }, 400);
    }
    
    var action = json.action;
    var data = json.data || {};
    
    Logger.log("Received action: " + action + ", user_id: " + (data.user_id || "unknown"));
    
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    
    if (action === "subscription") {
      _appendSubscription(ss, data);
      Logger.log("Subscription appended successfully");
    } else if (action === "status") {
      _appendStatus(ss, data);
      Logger.log("Status appended successfully");
    } else {
      Logger.log("Error: Unknown action: " + action);
      return _jsonResponse({ ok: false, error: "Unknown action: " + action }, 400);
    }
    
    return _jsonResponse({ ok: true });
  } catch (err) {
    Logger.log("Error in doPost: " + String(err) + ", stack: " + (err.stack || ""));
    return _jsonResponse({ ok: false, error: String(err) }, 500);
  }
}

function _jsonResponse(obj, code) {
  code = code || 200;
  var output = ContentService.createTextOutput(JSON.stringify(obj));
  output.setMimeType(ContentService.MimeType.JSON);
  return output;
}

function _getOrCreateSheet(ss, name, headers) {
  var sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  } else if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, headers.length).setValues([headers]);
  }
  return sheet;
}

function _appendSubscription(ss, data) {
  try {
    var headers = ["timestamp", "user_id", "username", "first_name", "specialty_id", "specialty_name", "notify_days"];
    var sheet = _getOrCreateSheet(ss, "Подписки", headers);
    
    // Log what we received
    Logger.log("Received notify_days: '" + (data.notify_days || "") + "' (type: " + typeof data.notify_days + ")");
    
    // Prepare row data - convert all to strings to avoid type issues
    var row = [
      String(data.timestamp || new Date().toISOString()),
      String(data.user_id || ""),
      String(data.username || ""),
      String(data.first_name || ""),
      String(data.specialty_id || ""),
      String(data.specialty_name || ""),
      String(data.notify_days || "")
    ];
    
    var lastRow = sheet.getLastRow() + 1;
    Logger.log("Appending to row: " + lastRow);
    
    // CRITICAL: Clear data validations for text columns BEFORE writing
    // This must be done for the entire column range to bypass column-level restrictions
    var textColumns = [3, 4, 6, 7]; // username, first_name, specialty_name, notify_days
    var maxRows = Math.max(sheet.getLastRow() + 10, 1000);
    
    for (var colIdx = 0; colIdx < textColumns.length; colIdx++) {
      var colNum = textColumns[colIdx];
      try {
        // Clear validations for a range that includes our new row
        var colRange = sheet.getRange(1, colNum, maxRows, 1);
        colRange.clearDataValidations();
        Logger.log("Cleared validations for column " + colNum);
      } catch(e) {
        Logger.log("Could not clear validations for column " + colNum + ": " + e);
      }
    }
    
    // Write each cell individually using multiple methods to ensure success
    for (var i = 0; i < row.length; i++) {
      try {
        var colIndex = i + 1;
        var cell = sheet.getRange(lastRow, colIndex);
        var value = row[i];
        var isTextColumn = textColumns.indexOf(colIndex) !== -1;
        
        // Clear validation for this specific cell again (redundant but safe)
        try {
          cell.clearDataValidations();
        } catch(e) {
          // Ignore
        }
        
        // For text columns, use multiple methods to ensure write succeeds
        if (isTextColumn) {
          var written = false;
          
          // Method 1: Try RichTextValue (bypasses most restrictions)
          if (!written) {
            try {
              var richTextValue = SpreadsheetApp.newRichTextValue()
                .setText(String(value))
                .build();
              cell.setRichTextValue(richTextValue);
              written = true;
              Logger.log("Wrote cell " + colIndex + " (" + headers[i] + ") using RichText: '" + value + "'");
            } catch(richTextErr) {
              // Continue to next method
            }
          }
          
          // Method 2: Set format then value
          if (!written) {
            try {
              cell.setNumberFormat("@"); // @ = text format
              cell.setValue(String(value));
              written = true;
              Logger.log("Wrote cell " + colIndex + " (" + headers[i] + ") using format+value: '" + value + "'");
            } catch(formatErr) {
              // Continue to next method
            }
          }
          
          // Method 3: Direct value (last resort)
          if (!written) {
            try {
              cell.setValue(value);
              written = true;
              Logger.log("Wrote cell " + colIndex + " (" + headers[i] + ") using direct value: '" + value + "'");
            } catch(directErr) {
              Logger.log("FAILED to write cell " + colIndex + " (" + headers[i] + "): " + directErr);
            }
          }
        } else {
          // For non-text columns, use regular setValue
          cell.setValue(value);
          Logger.log("Wrote cell " + colIndex + " (" + headers[i] + "): '" + value + "'");
        }
      } catch(cellErr) {
        Logger.log("Error writing cell " + (i + 1) + " (" + headers[i] + "): " + cellErr);
        // Continue with other cells even if one fails
      }
    }
    
    Logger.log("Successfully wrote all cells for row " + lastRow);
  } catch(err) {
    Logger.log("Error in _appendSubscription: " + String(err) + ", stack: " + (err.stack || ""));
    throw err; // Re-throw to be caught by doPost
  }
}

function _appendStatus(ss, data) {
  var headers = ["timestamp", "user_id", "status", "value"];
  var sheet = _getOrCreateSheet(ss, "Статус", headers);
  
  var row = [
    String(data.timestamp || new Date().toISOString()),
    String(data.user_id || ""),
    String(data.status || ""),
    String(data.value || "")
  ];
  
  var lastRow = sheet.getLastRow() + 1;
  var range = sheet.getRange(lastRow, 1, 1, row.length);
  
  // Clear validation only for this specific row
  try {
    range.clearDataValidations();
  } catch(e) {
    // Ignore if can't clear validations
  }
  
  // Write all values at once
  try {
    range.setValues([row]);
  } catch(e) {
    // If setValues fails, try writing cell by cell
    for (var i = 0; i < row.length; i++) {
      try {
        sheet.getRange(lastRow, i + 1).setValue(row[i]);
      } catch(cellErr) {
        Logger.log("Error writing cell " + (i + 1) + ": " + cellErr);
      }
    }
  }
}
