
def updateNewSheetStyle(sheetId, service, SAMPLE_SPREADSHEET_ID):
    requests = [ [
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 1,
              "startColumnIndex": 0,
              "endColumnIndex": 9
            },
            "cell": {
              "userEnteredFormat": {
                "backgroundColor": {
                  "red": 1,
                  "green": 0.95,
                  "blue": 0.8 
                },
                "horizontalAlignment" : "CENTER",
                "textFormat": {
                  "foregroundColor": {
                    "red": 0,
                    "green": 0,
                    "blue": 0
                  },
                  "fontSize": 14,
                  "bold": "true"
                }
              }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 1,
              "endRowIndex": 4,
              "startColumnIndex": 0,
              "endColumnIndex": 9
            },
            "cell": {
              "userEnteredFormat": {
                "backgroundColor": {
                  "red": 1,
                  "green": 0.95,
                  "blue": 0.8 
                },
                "horizontalAlignment" : "CENTER"
              }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 51,
              "startColumnIndex": 0,
              "endColumnIndex": 1
            },
            "cell": {
              "userEnteredFormat": {
                "backgroundColor": {
                  "red": 1,
                  "green": 0.95,
                  "blue": 0.8 
                },
                "horizontalAlignment" : "CENTER"
              }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 1,
              "endRowIndex": 3,
              "startColumnIndex": 1,
              "endColumnIndex": 5
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 1,
                      "green": 0.95,
                      "blue": 0.8 
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 0.01,
                        "green": 0.9,
                        "blue": 0.3
                      },
                      "fontSize": 12,
                      "bold": "true"
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 1,
              "endRowIndex": 3,
              "startColumnIndex": 5,
              "endColumnIndex": 9
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 1,
                      "green": 0.95,
                      "blue": 0.8 
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 0.9,
                        "green": 0,
                        "blue": 0
                      },
                      "fontSize": 12,
                      "bold": "true"
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 4,
              "endRowIndex": 5,
              "startColumnIndex": 9,
              "endColumnIndex": 11
            },
            "cell": {
                "userEnteredFormat": {
                    "backgroundColor": {
                      "red": 1,
                      "green": 0.95,
                      "blue": 0.8 
                    },
                    "horizontalAlignment" : "CENTER",
                    "textFormat": {
                      "foregroundColor": {
                        "red": 0,
                        "green": 0,
                        "blue": 0
                      },
                      "fontSize": 12,
                      "bold": "true"
                    }
                }
            },
            "fields": "userEnteredFormat(backgroundColor,textFormat,horizontalAlignment)"
          }
        },
        {
          "repeatCell": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 100,
              "startColumnIndex": 0,
              "endColumnIndex": 9
            },
            "cell": {
                "userEnteredFormat": {
                    "horizontalAlignment" : "CENTER"
                }
            },
            "fields": "userEnteredFormat(horizontalAlignment)"
          }
        },
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 51,
              "startColumnIndex": 1,
              "endColumnIndex": 9
            },
            "innerHorizontal": {
              "style": "SOLID",
              "width": 1,
              "color": {
                "green": 0
              },
            }
          }
        },
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 3,
              "endRowIndex": 9,
              "startColumnIndex": 9,
              "endColumnIndex": 11
            },
            "innerHorizontal": {
              "style": "SOLID",
              "width": 1,
              "color": {
                "green": 0
              },
            }
          }
        },
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 0,
              "endRowIndex": 51,
              "startColumnIndex": 0,
              "endColumnIndex": 10
            },
            "innerVertical": {
              "style": "SOLID",
              "width": 1,
              "color": {
                "green": 0
              },
            }
          }
        },
        {
          "updateBorders": {
            "range": {
              "sheetId": sheetId,
              "startRowIndex": 4,
              "endRowIndex": 8,
              "startColumnIndex": 8,
              "endColumnIndex": 12
            },
            "innerVertical": {
              "style": "SOLID",
              "width": 1,
              "color": {
                "green": 0
              },
            }
          }
        },
        {
          "updateDimensionProperties": {
            "range": {
              "sheetId": sheetId,
              "dimension": "COLUMNS",
              "startIndex": 1,
              "endIndex": 9
            },
            "properties": {
              "pixelSize": 100
            },
            "fields": "pixelSize"
          }
        },
        {
          "updateDimensionProperties": {
            "range": {
              "sheetId": sheetId,
              "dimension": "ROWS",
              "startIndex": 4,
              "endIndex": 51
            },
            "properties": {
              "pixelSize": 35
            },
            "fields": "pixelSize"
          }
        }

        
      ]
    ]
    
    body = {
        'requests': requests
    }

    request = service.spreadsheets().batchUpdate(spreadsheetId=SAMPLE_SPREADSHEET_ID, body=body)
    response = request.execute()
