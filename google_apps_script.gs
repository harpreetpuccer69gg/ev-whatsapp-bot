function onLeadSubmit() {
  const masterSheet = SpreadsheetApp.getActiveSpreadsheet();
  const allSheets = masterSheet.getSheets();
  const leadsSheet = allSheets.find(s => s.getName().trim() === 'Leads');
  const vendorMap = allSheets.find(s => s.getName().trim() === 'Vendor_Map');

  if (!leadsSheet || !vendorMap) { Logger.log('Sheet not found'); return; }

  const allData = leadsSheet.getDataRange().getValues();
  const ourHeaders = allData[0];

  let transferCol = ourHeaders.findIndex(h => h.toString().trim() === 'Transferred');
  if (transferCol === -1) {
    transferCol = ourHeaders.length;
    leadsSheet.getRange(1, transferCol + 1).setValue('Transferred');
  }

  let emailCol = ourHeaders.findIndex(h => h.toString().trim() === 'Email Sent');
  if (emailCol === -1) {
    emailCol = transferCol + 1;
    leadsSheet.getRange(1, emailCol + 1).setValue('Email Sent');
  }

  const mapData = vendorMap.getDataRange().getValues();

  function normalizeVendor(name) {
    const n = name.toString().trim().toLowerCase();
    if (n === 'voltup' || n === 'volt up')                       return 'voltup';
    if (n === 'gogreen' || n === 'go green')                     return 'gogreen';
    if (n === 'eco ev' || n === 'ecoev')                         return 'ecoev';
    if (n === 'yuwwaa' || n === 'yuvwaaspeed' || n === 'yuvwaa') return 'yuvwaa';
    if (n === 'bijliride' || n === 'bijli ride')                  return 'bijliride';
    if (n === 'e-went' || n === 'ewent')                         return 'ewent';
    if (n === 'yugorides' || n === 'yugo')                       return 'yugorides';
    return n.replace(/\s+/g, '').replace(/-/g, '');
  }

  function getValueForHeader(header, row) {
    const h = header.toString().trim().toLowerCase();
    if (h === 'date' || h === 'timestamp')                       return row[0];
    if (h === 'rider name' || h === 'name')                      return row[1];
    if (h === 'phone' || h === 'rider phone' || h === 'mobile')  return row[2];
    if (h === 'city')                                             return row[3];
    if (h === 'language')                                         return row[4];
    if (h === 'budget' || h === 'budget range')                   return row[5];
    if (h === 'vendor')                                           return row[7];
    if (h === 'make' || h === 'model' || h === 'vehicle')         return row[8];
    if (h === 'type')                                             return row[9];
    if (h === 'rental/week' || h === 'rent' || h === 'rental')    return row[10];
    if (h === 'security deposit' || h === 'deposit')              return row[11];
    if (h === 'refundable deposit' || h === 'refundable')         return row[12];
    if (h === 'spoc name')                                        return row[13];
    if (h === 'spoc phone')                                       return row[14];
    if (h === 'status' || h === 'conversion status')              return 'New Lead';
    if (h === 'store name')                                       return '';
    if (h === 'license?' || h === 'license')                      return '';
    if (h === 'flipkart id')                                      return '';
    if (h === 'attempted by')                                     return '';
    if (h === 'remarks 1' || h === 'remarks 2')                   return '';
    return '';
  }

  // ── NEW: send city-wise count summary (no rider details) ──
  function sendSummaryEmail(vendorName, emailAddresses, cityCountMap) {
    if (!emailAddresses) return false;
    const emails = emailAddresses.split(',').map(e => e.trim()).filter(e => e);
    if (emails.length === 0) return false;

    const total = Object.values(cityCountMap).reduce((a, b) => a + b, 0);
    const now = new Date();
    const timeStr = Utilities.formatDate(now, Session.getScriptTimeZone(), 'dd MMM yyyy hh:mm a');

    const subject = `🛵 ${vendorName} — ${total} New Lead(s) | ${timeStr} | Flipkart Minutes`;

    let cityLines = '';
    Object.keys(cityCountMap).sort().forEach(city => {
      cityLines += `  • ${city}: ${cityCountMap[city]} lead(s)\n`;
    });

    const body =
`Hi ${vendorName} Team,

You have received ${total} new lead(s) in the last hour from Flipkart Minutes EV Assist.

━━━━━━━━━━━━━━━━━━━━━━━━
LEADS SUMMARY (City-wise)
━━━━━━━━━━━━━━━━━━━━━━━━
${cityLines}
Total New Leads : ${total}
━━━━━━━━━━━━━━━━━━━━━━━━

Please check your sheet for full rider details and contact them within 24 hours.

— Flipkart Minutes EV Assist
https://ev-rental-in-minutes.onrender.com`;

    emails.forEach(email => {
      try {
        GmailApp.sendEmail(email, subject, body);
        Logger.log('Email sent to: ' + email);
      } catch(e) {
        Logger.log('Email error for ' + email + ': ' + e.message);
      }
    });
    return true;
  }

  // ── STEP 1: Transfer rows to vendor sheets ──
  for (let i = 1; i < allData.length; i++) {
    const row = allData[i];
    const alreadyTransferred = row[transferCol] === 'YES';
    if (alreadyTransferred) continue;

    const vendorName = (row[7] || '').toString().trim();
    if (!vendorName) continue;

    let vendorSheetId = null;
    let targetTab = 'Leads';
    let vendorEmail = '';

    for (let j = 1; j < mapData.length; j++) {
      if (normalizeVendor(mapData[j][0]) === normalizeVendor(vendorName)) {
        vendorSheetId = mapData[j][1].toString().trim();
        vendorEmail   = mapData[j][2].toString().trim();
        targetTab     = (mapData[j][3] || 'Leads').toString().trim();
        break;
      }
    }

    if (!vendorSheetId && !vendorEmail) {
      Logger.log('Vendor not in map: ' + vendorName);
      leadsSheet.getRange(i + 1, transferCol + 1).setValue('NO_VENDOR');
      continue;
    }

    if (vendorSheetId) {
      try {
        const vendorSpreadsheet = SpreadsheetApp.openById(vendorSheetId);
        let vendorSheet = vendorSpreadsheet.getSheetByName(targetTab);
        if (!vendorSheet) {
          vendorSheet = vendorSpreadsheet.insertSheet(targetTab);
          vendorSheet.appendRow(ourHeaders.slice(0, transferCol));
          vendorSheet.appendRow(row.slice(0, transferCol));
        } else {
          const vendorHeaders = vendorSheet.getRange(1, 1, 1, vendorSheet.getLastColumn()).getValues()[0];
          const mappedRow = vendorHeaders.map(h => getValueForHeader(h, row));
          vendorSheet.appendRow(mappedRow);
        }
        leadsSheet.getRange(i + 1, transferCol + 1).setValue('YES');
        Logger.log('Sheet SUCCESS: ' + vendorName);
      } catch(err) {
        Logger.log('Sheet ERROR for ' + vendorName + ': ' + err.message);
        leadsSheet.getRange(i + 1, transferCol + 1).setValue('ERROR: ' + err.message);
      }
    }
  }

  // ── STEP 2: Batch email — group unsent leads by vendor+city, send ONE summary email per vendor ──
  const freshData = leadsSheet.getDataRange().getValues(); // re-read after transfers

  // vendorKey -> { name, email, cityCount: {city: count}, rowIndices: [] }
  const vendorBatch = {};

  for (let i = 1; i < freshData.length; i++) {
    const row = freshData[i];
    const alreadyEmailed = row[emailCol] === 'YES';
    if (alreadyEmailed) continue;

    const vendorName = (row[7] || '').toString().trim();
    const city       = (row[3] || '').toString().trim();
    if (!vendorName || !city) continue;

    const vKey = normalizeVendor(vendorName);

    if (!vendorBatch[vKey]) {
      // Find email from vendor map
      let vendorEmail = '';
      let matchedName = vendorName;
      for (let j = 1; j < mapData.length; j++) {
        if (normalizeVendor(mapData[j][0]) === vKey) {
          vendorEmail  = mapData[j][2].toString().trim();
          matchedName  = mapData[j][0].toString().trim();
          break;
        }
      }
      if (!vendorEmail) continue; // no email, skip
      vendorBatch[vKey] = { name: matchedName, email: vendorEmail, cityCount: {}, rowIndices: [] };
    }

    vendorBatch[vKey].cityCount[city] = (vendorBatch[vKey].cityCount[city] || 0) + 1;
    vendorBatch[vKey].rowIndices.push(i + 1); // 1-based sheet row
  }

  // Send one email per vendor with city-wise summary
  for (const vKey in vendorBatch) {
    const { name, email, cityCount, rowIndices } = vendorBatch[vKey];
    const sent = sendSummaryEmail(name, email, cityCount);
    if (sent) {
      rowIndices.forEach(rowNum => {
        leadsSheet.getRange(rowNum, emailCol + 1).setValue('YES');
      });
      Logger.log(`Emailed ${name}: ${JSON.stringify(cityCount)}`);
    }
  }

  Logger.log('Done');
}

function createTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('onLeadSubmit')
    .timeBased()
    .everyHours(1)
    .create();
  Logger.log('Trigger created - runs every 1 hour');
}
