// Function to fetch exchange rate data from the API
function getExchangeRates(currency) {
  const url = `https://api.exchangerate-api.com/v4/latest/${currency}`;

  try {
    // Fetch the data from the endpoint
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());

    // Return data as an object
    return data;
  } catch (error) {
    // Handle error
    return `Error: ${error.message}`;
  }
}

// Custom function to get the exchange rate for a specific currency
function getExchangeRate(currency) {
  const data = getExchangeRates(currency);

  if (data && data.rates && data.rates["EUR"]) {
    return data.rates["EUR"];
  } else {
    return `Error: Unable to find rate for EUR`;
  }
}

function onEdit(e) {
  // Define constants for sheet names
  const PLANNING_SHEET_NAME = "Mansour Planning";
  const DAILY_SHEET_NAME = "Daily routine";

  // Get the active sheet and range from the event object
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  const sheetName = sheet.getName();

  // Map sheet names to their corresponding handlers
  const handlers = {
    [PLANNING_SHEET_NAME]: onPlanningEdit,
    [DAILY_SHEET_NAME]: onDailyEdit,
  };

  // Execute the appropriate handler if the sheet name matches
  const handler = handlers[sheetName];
  if (handler) {
    handler(range, sheet);
  }
}
function onPlanningEdit(range, sheet) {
  const dateColumn = 3;
  const createdDateColumn = 2;
  const priorityColumn = 4;
  const statusCoulmn = 5;
  // Get the row and column of the edited cell
  const editedRow = range.getRow();
  const editedColumn = range.getColumn();

  // Ensure it's not updating the header row
  if (editedRow > 1) {
    // Update the date column with the current date using =DATE() format
    const currentDate = new Date();
    const dateCell = sheet.getRange(editedRow, dateColumn);

    // Set the formula to =DATE(year, month, day)
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth() + 1; // Months are 0-indexed
    const day = currentDate.getDate();
    dateCell.setFormula(`=DATE(${year}, ${month}, ${day})`);

    // created date
    const createdDateCell = sheet.getRange(editedRow, createdDateColumn);
    if (!createdDateCell.getValue()) {
      // Add current date in =DATE() format
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1; // Months are 0-indexed
      const day = currentDate.getDate();
      createdDateCell.setFormula(`=DATE(${year}, ${month}, ${day})`);
      // default priority
      const priorityCell = sheet.getRange(editedRow, priorityColumn);
      priorityCell.setValue("Low");
      // default status
      const statusCell = sheet.getRange(editedRow, statusCoulmn);
      statusCell.setValue("Not-started");
    }
  }
}
function onDailyEdit(range, sheet) {
  const dateColumn = 4;

  // Get the row and column of the edited cell
  const editedRow = range.getRow();
  const editedColumn = range.getColumn();

  // Ensure it's not updating the header row
  if (editedRow > 1) {
    // created date
    const dateCell = sheet.getRange(editedRow, dateColumn);
    if (!dateCell.getValue()) {
      const currentDate = new Date();
      // Add current date in =DATE() format
      const year = currentDate.getFullYear();
      const month = currentDate.getMonth() + 1; // Months are 0-indexed
      const day = currentDate.getDate();
      dateCell.setFormula(`=DATE(${year}, ${month}, ${day})`);
    }
  }
}

/**
 * Fetches the latest BNB/USDT price from KuCoin.
 *
 * @return {number} The current price of BNB in USDT.
 * @customfunction
 */
function getBNBPriceKuCoin() {
  const url =
    "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=BNB-USDT";
  try {
    const response = UrlFetchApp.fetch(url);
    const data = JSON.parse(response.getContentText());
    return parseFloat(data.data.price);
  } catch (error) {
    return `Error: ${error.message}`;
  }
}

function insertRows() {
  // number of rows from 18 to 6
  const numberOfRows = 2;
  // get active sheet
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();

  let hour = 23;
  for (let i = 1; i <= numberOfRows; i++) {
    const minute = i % 2 === 0 ? 0 : 30;
    const rowContent = ["", `=TIME(${hour}, ${minute}, 0)`]; // Data to populate in the new row

    // Insert a new row in the second position
    // sheet.insertRowAfter(1);

    // // Populate the second row with data
    // const rowRange = sheet.getRange(2, 1, 1, rowContent.length); // Target the second row

    // rowRange.setValues([rowContent]);
    copyRowToSecondPosition();
    // rowRange.setFontWeight("normal");
    if (i % 2 === 0) {
      hour = hour - 1;
    }
  }
}

function copyRowToSecondPosition() {
  try {
    // Get the active spreadsheet and sheet
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getActiveSheet();

    // Get the row to copy (for example, row 1)
    const sourceRowNum = 1; // Change this to the row number you want to copy
    const lastColumn = sheet.getLastColumn();

    // Get the source row data
    const sourceRange = sheet.getRange(sourceRowNum, 1, 1, lastColumn);
    const sourceValues = sourceRange.getValues();
    const sourceFormats = sourceRange.getBackgrounds();
    const sourceFormulas = sourceRange.getFormulas();

    // Insert a new row at position 2
    sheet.insertRowAfter(1);

    // Get the target range (row 2)
    const targetRange = sheet.getRange(2, 1, 1, lastColumn);

    // Copy values, formats, and formulas
    targetRange.setValues(sourceValues);
    targetRange.setBackgrounds(sourceFormats);

    // Apply formulas only where they exist
    for (let col = 0; col < sourceFormulas[0].length; col++) {
      if (sourceFormulas[0][col] !== "") {
        targetRange.getCell(1, col + 1).setFormula(sourceFormulas[0][col]);
      }
    }

    // Copy data validations if any
    const validations = sourceRange.getDataValidations();
    targetRange.setDataValidations(validations);

    // Show success message
    SpreadsheetApp.getActive().toast("Row copied successfully!");
  } catch (error) {
    Logger.log("Error: " + error.toString());
    SpreadsheetApp.getActive().toast("Error copying row: " + error.toString());
  }
}
