#include <windows.h>
#include <sqlext.h>
#include <stdio.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define BRWS_LEN 1024

/*
---------------------------------------------------------
   TestSQLBrowseConnect
---------------------------------------------------------
*/
PassFail TestSQLBrowseConnect(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE		returncode;
	SQLHANDLE 	henv = (SQLHANDLE)NULL, henv1[NUM_ENV_HND];
	SQLHANDLE 	hdbc = (SQLHANDLE)NULL, badhdbc, hdbc1[NUM_ENV_HND * NUM_CONN_HND];
	SQLHANDLE	hstmt = (SQLHANDLE)NULL;
	SQLTCHAR 	szConnStrIn[BRWS_LEN], szConnStrOut[BRWS_LEN];
	TCHAR		connstr[BRWS_LEN];
	TCHAR		tstConnStr[BRWS_LEN];
	SWORD		cbConnStrOut;
	int i = 0, j = 0;

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLBrowseConnect.\n"));

	TEST_INIT;


//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLBrowseConnect: Invalid CONN handle pointer\n");
	badhdbc = (SQLHANDLE)NULL;
	//_tcscpy(connstr,"");
	//_tcscat(connstr,"DSN=");
	//_tcscat(connstr,pTestInfo->DataSource);
	//_tcscat(connstr,";");
	//_tcscat(connstr,"UID=");
	//_tcscat(connstr,pTestInfo->UserID);
	//_tcscat(connstr,";");
	//_tcscat(connstr,"PWD=");
	//_tcscat(connstr,pTestInfo->Password);
	//_tcscat(connstr,";");
    _tcscpy(connstr,_T(""));
    _stprintf(connstr, _T("DSN=%s;UID=%s;PWD=%s;"),pTestInfo->DataSource,pTestInfo->UserID,pTestInfo->Password);
	_tcscpy((TCHAR*)szConnStrIn,_T(""));
	_tcscat((TCHAR*)szConnStrIn,connstr);
	returncode = SQLBrowseConnect(badhdbc, szConnStrIn, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(badhdbc);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLBrowseConnect: NULL szConnStrIn\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLBrowseConnect(hdbc, NULL, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLBrowseConnect: Invalid szConnStrIn length\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLBrowseConnect(hdbc, szConnStrIn, (SWORD)(_tcslen(pTestInfo->DataSource)+4), szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLBrowseConnect: zero length\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLBrowseConnect(hdbc, szConnStrIn,0, szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Negative Functionality of SQLBrowseConnect: Invalid DSN\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}
	_tcscpy(connstr,_T(""));
	_tcscat(connstr,_T("DSN="));
	_tcscat(connstr,_T("baddsn"));
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("UID="));
	_tcscat(connstr,pTestInfo->UserID);
	_tcscat(connstr,_T(";"));
	_tcscat(connstr,_T("PWD="));
	_tcscat(connstr,pTestInfo->Password);
	_tcscat(connstr,_T(";"));
	returncode = SQLBrowseConnect(hdbc,(SQLTCHAR*)connstr,SQL_NTS,szConnStrOut,BRWS_LEN,&cbConnStrOut);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;


//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect with SQL_NTS\n");

	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLBrowseConnect(hdbc,szConnStrIn,SQL_NTS,szConnStrOut,BRWS_LEN,&cbConnStrOut);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		_tprintf(_T("\nIn string = %s\n"),szConnStrIn);
		_tprintf(_T("Out string = %s\n"),szConnStrOut);
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;


//==========================================================================================
   TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect with _tcslen\n");
	returncode = SQLAllocEnv(&henv);                 // Environment handle 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    // Connection handle  
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		LogAllErrors(henv,hdbc,hstmt);
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLBrowseConnect(hdbc,szConnStrIn,(SWORD)_tcslen((TCHAR*)szConnStrIn),szConnStrOut,BRWS_LEN,&cbConnStrOut);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect to check need data\n");
	returncode = SQLAllocEnv(&henv);                 /* Environment handle */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
		TEST_FAILED;
		TEST_RETURN;
		}

	_stprintf(tstConnStr,_T("DSN=%s;"),pTestInfo->DataSource);

	//_tprintf(_T("\nIn string = %s\n"),tstConnStr);

	returncode = SQLBrowseConnect(hdbc, (SQLTCHAR*)tstConnStr, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if(!CHECKRC(SQL_NEED_DATA,returncode,"SQLBrowseConnect")){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	_tcscat(tstConnStr,_T("UID="));
	_tcscat(tstConnStr,pTestInfo->UserID);
	_tcscat(tstConnStr,_T(";"));

		//_tprintf(_T("\nIn string = %s\n"),tstConnStr);

	returncode = SQLBrowseConnect(hdbc, (SQLTCHAR*)tstConnStr, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
	if((returncode != SQL_NEED_DATA) && (returncode != SQL_SUCCESS)){
		TEST_FAILED;
		LogAllErrors(henv,hdbc,hstmt);
		}

	if(returncode == SQL_NEED_DATA)
	{
		_tcscat(tstConnStr,_T("PWD="));
		_tcscat(tstConnStr,pTestInfo->Password);
		_tcscat(tstConnStr,_T(";"));

		//_tprintf(_T("\nIn string = %s\n"),tstConnStr);

		returncode = SQLBrowseConnect(hdbc, (SQLTCHAR*)tstConnStr, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBrowseConnect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}

	SQLDisconnect(hdbc);
	SQLFreeConnect(hdbc);
	SQLFreeEnv(henv);
	TESTCASE_END;

//==========================================================================================

	TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect, SQLDisconnect then SQLBrowseConnect.\n");
	for (i = 0; i < 3; i++)
	{
		returncode = SQLAllocEnv(&henv);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
		{
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
		{
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}
		returncode = SQLBrowseConnect(hdbc, szConnStrIn, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
		{
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
		switch (i)
		{
			case 0:
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLBrowseConnect(hdbc, szConnStrIn, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				break;
			case 1:
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLFreeConnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLBrowseConnect(hdbc, szConnStrIn, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				break;
			case 2:
				returncode = SQLDisconnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLFreeConnect(hdbc);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLFreeEnv(henv);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				returncode = SQLAllocEnv(&henv);                 /* Environment handle */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
				{
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLAllocConnect(henv, &hdbc);    /* Connection handle  */
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
				{
					LogAllErrors(henv,hdbc,hstmt);
					TEST_FAILED;
					TEST_RETURN;
				}
				returncode = SQLBrowseConnect(hdbc, szConnStrIn, SQL_NTS, szConnStrOut, BRWS_LEN, &cbConnStrOut);
				if(!CHECKRC(SQL_SUCCESS,returncode,"SQLConnect"))
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				break;
			default:
				// End
				break;
		}
		SQLDisconnect(hdbc);
		SQLFreeConnect(hdbc);
		SQLFreeEnv(henv);
	}
  TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect with different connection handles\n");
	returncode = SQLAllocEnv(&henv);               
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv")){
		TEST_FAILED;
		TEST_RETURN;
		}

	for (i = 0; i < NUM_CONN_HND; i++){
		returncode = SQLAllocConnect(henv, &hdbc1[i]);    
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect")){
			LogAllErrors(henv,hdbc,hstmt);
			TEST_FAILED;
			TEST_RETURN;
		}

		returncode = SQLBrowseConnect(hdbc1[i],szConnStrIn,SQL_NTS,szConnStrOut,BRWS_LEN,&cbConnStrOut);
		//_tprintf(_T("\n\nret=%d  i=%d %s\n%s\n\n"), returncode, i, szConnStrIn, szConnStrOut);		
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBrowseConnect")){
			TEST_FAILED;
			LogAllErrors(henv,hdbc,hstmt);
		}
	}
	for (i = 0; i < NUM_CONN_HND; i++){
		//_tprintf(_T("%d %d\n"), i, NUM_CONN_HND);
		SQLDisconnect(hdbc1[i]);
		SQLFreeConnect(hdbc1[i]);
	}
	SQLFreeEnv(henv);
   TESTCASE_END;
//==========================================================================================
   TESTCASE_BEGIN("Test Positive Functionality of SQLBrowseConnect with different env & conn handles\n");
	for (j = 0; j < NUM_ENV_HND / 5; j++)
	{
		returncode = SQLAllocEnv(&henv1[j]);                 /* Environment handle */
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocEnv"))
		{
			TEST_FAILED;
			TEST_RETURN;
		}
		for (i = 0; i < NUM_CONN_HND / 2; i++)
		{
			returncode = SQLAllocConnect(henv1[j], &hdbc1[j * NUM_CONN_HND + i]);    /* Connection handle  */
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocConnect"))
			{
				LogAllErrors(henv1[j],hdbc1[j * NUM_CONN_HND + i],hstmt);
				TEST_FAILED;
				TEST_RETURN;
			}
			returncode = SQLBrowseConnect(hdbc1[j * NUM_CONN_HND + i],szConnStrIn,SQL_NTS,szConnStrOut,BRWS_LEN,&cbConnStrOut);
			if(!CHECKRC(SQL_SUCCESS,returncode,"SQLBrowseConnect"))
			{
				TEST_FAILED;
				LogAllErrors(henv1[j],hdbc1[j * NUM_CONN_HND + i],hstmt);
			}
		}
	}
	for (j = 0; j < NUM_ENV_HND / 5; j++)
	{
		for (i = 0; i < NUM_CONN_HND / 2; i++)
		{
			//_tprintf(_T("%d %d %d \n"), j, i, NUM_CONN_HND);
			SQLDisconnect(hdbc1[j * NUM_CONN_HND + i]);
			SQLFreeConnect(hdbc1[j * NUM_CONN_HND + i]);
		}
		SQLFreeEnv(henv1[j]);
	}
   TESTCASE_END;
	 LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End of testing API ===> SQLBrowseConnect \n"));  
//==========================================================================================


   TEST_RETURN;

}
