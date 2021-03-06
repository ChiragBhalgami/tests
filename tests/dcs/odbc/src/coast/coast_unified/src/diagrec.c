#include <windows.h>
#include <sqlext.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	SQL_MAX_MESSAGE_LEN 300

/*
---------------------------------------------------------
   TestSQLGetDiagRec 
---------------------------------------------------------
*/
PassFail TestMXSQLGetDiagRec(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE			returncode;
	SQLHANDLE 		henv;
	SQLHANDLE 		hdbc;
	SQLHANDLE		hstmt;
	SQLTCHAR			SqlState[STATE_SIZE];
	SQLINTEGER		NativeError;
	SQLTCHAR			ErrorMsg[MAX_STRING_SIZE];
	SQLSMALLINT		ErrorMsglen;
	TCHAR			*ExecDirStr[4];

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLGetDiagRec"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecDirStr[0] = var_mapping(_T("SQLGetDiagRec_ExecDirStr_1"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLGetDiagRec_ExecDirStr_2"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLGetDiagRec_ExecDirStr_3"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLGetDiagRec_ExecDirStr_4"), var_list);
//=================================================================================================

 LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLGetDiagRec.\n"));
	
 TEST_INIT;

 if(!FullConnectWithOptions(pTestInfo, CONNECT_ODBC_VERSION_3))
 {
	LogMsg(NONE,_T("Unable to connect\n"));
	TEST_FAILED;
	TEST_RETURN;
 }

 henv = pTestInfo->henv;
 hdbc = pTestInfo->hdbc;
 hstmt = (SQLHANDLE)pTestInfo->hstmt;

 returncode = SQLAllocHandle(SQL_HANDLE_STMT, (SQLHANDLE)hdbc, &hstmt);
 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLAllocHandle"))
 {
 	LogAllErrorsVer3(henv,hdbc,hstmt);
	FullDisconnect(pTestInfo);
	TEST_FAILED;
	TEST_RETURN;
 }
 
 TESTCASE_BEGIN("Test syntax while creating a table SQLError\n");
 returncode = SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)ExecDirStr[0],SQL_NTS);
 if (returncode == SQL_ERROR)
 {
	returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,1, SqlState, &NativeError, ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
	{
		TEST_FAILED;
		LogAllErrorsVer3(henv,hdbc,hstmt);
	}
	else
	{
		LogMsg(NONE,_T("SqlState: %s and ErrorMsg: %s\n"),SqlState,ErrorMsg);
		TESTCASE_END;
	}
 }

 TESTCASE_BEGIN("Test syntax while inserting a table SQLError\n");
 SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)ExecDirStr[3],SQL_NTS);//clean
 returncode = SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)ExecDirStr[1],SQL_NTS);
 if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
 {
 	TEST_FAILED;
	LogAllErrorsVer3(henv,hdbc,hstmt);
 }

 returncode = SQLExecDirect(hstmt,(SQLTCHAR*)(SQLTCHAR *)ExecDirStr[2],SQL_NTS);
 if (returncode == SQL_ERROR)
 {
	returncode = SQLGetDiagRec(SQL_HANDLE_STMT, hstmt,1, SqlState, &NativeError, ErrorMsg, MAX_STRING_SIZE, &ErrorMsglen);
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLError"))
	{
		TEST_FAILED;
		LogAllErrorsVer3(henv,hdbc,hstmt);
	}
	else
	{
		LogMsg(NONE,_T("SqlState: %s and ErrorMsg: %s\n"),SqlState,ErrorMsg);
		if(_tcscmp((TCHAR*)SqlState,_T("22001")))
		TEST_FAILED;
		TESTCASE_END;
	}
 }
 else {
	LogMsg(ERRMSG,_T("Expect: SQL_ERROR and Actual: %d, line=%d\n"),returncode, __LINE__);
	TEST_FAILED;
	TESTCASE_END;
 }

 SQLExecDirect(hstmt,(SQLTCHAR*) (SQLTCHAR *)ExecDirStr[3],SQL_NTS); // Cleanup
 SQLFreeHandle(SQL_HANDLE_STMT, hstmt);
 
 LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLGetDiagRec.\n"));
 
 FullDisconnect3(pTestInfo);
 free_list(var_list);
 TEST_RETURN;
}
