#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
//#include <winbase.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

#define	NAME_LEN		300

/*
---------------------------------------------------------
   TestSQLGetDiagField
---------------------------------------------------------
*/
PassFail TestMXSQLGetDiagField(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	RETCODE				returncode;
	SQLHANDLE 			henv;
	SQLHANDLE 			hdbc;
	SQLHANDLE			hstmt;
	SQLLEN				DiagInfoIntPtr64; //sushil
	SQLINTEGER   		DiagInfoIntPtr;
	SQLRETURN			DiagInfoReturnPtr;
	SQLTCHAR	*			DiagInfoCharPtr;
	SQLSMALLINT  		StringLengthPtr;
	TCHAR				*ExecDirStr[9];

	int	i = 0;
//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLGetDiagField"), charset_file);
	if (var_list == NULL) return FAILED;

	//print_list(var_list);
	ExecDirStr[0] = var_mapping(_T("SQLGetDiagField_ExecDirStr_1"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLGetDiagField_ExecDirStr_2"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLGetDiagField_ExecDirStr_3"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLGetDiagField_ExecDirStr_4"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLGetDiagField_ExecDirStr_5"), var_list);
	ExecDirStr[5] = var_mapping(_T("SQLGetDiagField_ExecDirStr_6"), var_list);
	ExecDirStr[6] = var_mapping(_T("SQLGetDiagField_ExecDirStr_7"), var_list);
	ExecDirStr[7] = var_mapping(_T("SQLGetDiagField_ExecDirStr_8"), var_list);
	ExecDirStr[8] = var_mapping(_T("SQLGetDiagField_ExecDirStr_9"), var_list);

//========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API => SQLGetDiagField.\n"));
	TEST_INIT;

	TESTCASE_BEGIN("Initializing SQLGetDiagField test environment\n");
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
	
	TESTCASE_END;

	DiagInfoCharPtr = (SQLTCHAR *)malloc(NAME_LEN);
	SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[6],SQL_NTS); /* CLEANUP */

//========================================================================================================
    
	TESTCASE_BEGIN("Checking SQLGetDiagField for invalid handle\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,SQL_NULL_HANDLE,0,SQL_DIAG_NUMBER,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if(!CHECKRC(SQL_INVALID_HANDLE,returncode,"SQLGetDiagField"))
		{
		LogMsg(ERRMSG, _T("Expected: %d and actual: %d are not matched\n"), SQL_INVALID_HANDLE, returncode);
		TEST_FAILED;
		}

	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for fetching diagnostic field from rec. no. ZERO\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,0,SQL_DIAG_COLUMN_NUMBER,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if(!CHECKRC(SQL_ERROR,returncode,"SQLGetDiagField"))
		{
		LogMsg(ERRMSG, _T("Expected: %d and actual: %d are not matched\n"), SQL_ERROR, returncode);
		TEST_FAILED;
		}

	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for record number greater than existing records\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,5,SQL_DIAG_CLASS_ORIGIN,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if(!CHECKRC(SQL_NO_DATA,returncode,"SQLGetDiagField"))
		{
		LogMsg(ERRMSG, _T("Expected: %d and actual: %d are not matched\n"), SQL_NO_DATA, returncode);
		TEST_FAILED;
		}
	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_NUMBER\n");

	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[8],SQL_NTS); 
	if(!CHECKRC(SQL_ERROR,returncode,"SQLExecDirect"))
		{
		LogMsg(ERRMSG, _T("Expected: %d and actual: %d are not matched\n"), SQL_ERROR, returncode);
		TEST_FAILED;
		}
	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,0,SQL_DIAG_NUMBER,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}

	if (DiagInfoIntPtr != 2)
		{
		LogMsg(ERRMSG, _T("DiagInfoIntPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), 2, DiagInfoIntPtr,__LINE__);
		TEST_FAILED;
		}
	
	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_MESSAGE_TEXT\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,1,SQL_DIAG_MESSAGE_TEXT,(SQLSMALLINT *)DiagInfoCharPtr,NAME_LEN,(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched %d \n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode, __LINE__);
		TEST_FAILED;
		}

	if ((_tcsstr((TCHAR*)DiagInfoCharPtr,_T("SQL ERROR")) == NULL) && 
		(_tcsstr((TCHAR*)DiagInfoCharPtr,_T("SQL error")) == NULL))
		{
		LogMsg(ERRMSG, _T("DiagInfoCharPtr value mismatched\n Message returned: %s, line = %d\n"), DiagInfoCharPtr, __LINE__);
		TEST_FAILED;
		}

	TESTCASE_END;
	
//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_NATIVE\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,1,SQL_DIAG_NATIVE,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}
	if ( DiagInfoIntPtr != -8822 ) 
		{
		LogMsg(ERRMSG, _T("DiagInfoIntPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), -8822, DiagInfoIntPtr,__LINE__);
		TEST_FAILED;
		}

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,2,SQL_DIAG_NATIVE,(SQLPOINTER*)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}
	if ( DiagInfoIntPtr != -15001 ) 
		{
		LogMsg(ERRMSG, _T("DiagInfoIntPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), -15001, DiagInfoIntPtr,__LINE__);
		TEST_FAILED;
		}


	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_SQLSTATE\n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,1,SQL_DIAG_SQLSTATE,(SQLSMALLINT *)DiagInfoCharPtr,NAME_LEN,(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}

	if (_tcsstr((TCHAR*)DiagInfoCharPtr,_T("X08MU")) == NULL) 		
		{
		LogMsg(ERRMSG, _T("DiagInfoCharPtr value mismatched. Expected: X08MU and Actual %s, line = %d\n"),DiagInfoCharPtr,__LINE__);
		TEST_FAILED;
		}

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,2,SQL_DIAG_SQLSTATE,(SQLSMALLINT *)DiagInfoCharPtr,NAME_LEN,(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}

	if (_tcsstr((TCHAR*)DiagInfoCharPtr,_T("42000")) == NULL) 
		{
		LogMsg(ERRMSG, _T("DiagInfoCharPtr value mismatched. Expected: 42000 and Actual %s, line = %d\n"),DiagInfoCharPtr,__LINE__);
		TEST_FAILED;
		}

	TESTCASE_END;

//========================================================================================================	
	
	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_RETURNCODE \n");

	returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,0,SQL_DIAG_RETURNCODE,(SQLSMALLINT *)&DiagInfoReturnPtr,sizeof(DiagInfoReturnPtr),(SQLSMALLINT *)&StringLengthPtr);
	if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		{
		LogMsg(ERRMSG, _T("Expected: %d or %d and actual: %d are not matched\n"), SQL_SUCCESS, SQL_SUCCESS_WITH_INFO, returncode);
		TEST_FAILED;
		}

	if (DiagInfoReturnPtr != SQL_ERROR)
		{
		LogMsg(ERRMSG, _T("DiagInfoReturnPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), SQL_ERROR, DiagInfoReturnPtr,__LINE__);
		TEST_FAILED;
		}
	
	returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[0],SQL_NTS); 
	if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
	{
	  TEST_FAILED;
	  LogAllErrorsVer3(henv,hdbc,hstmt);
	}

	TESTCASE_END;

//========================================================================================================

	TESTCASE_BEGIN("Checking SQLGetDiagField for SQL_DIAG_ROW_COUNT \n");
	
    for ( i = 1; i < 7; i++)
    {
	    returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[i],SQL_NTS); 
		if(!CHECKRC(SQL_SUCCESS,returncode,"SQLExecDirect"))
		{
			TEST_FAILED;
			LogAllErrorsVer3(henv,hdbc,hstmt);
		}
		DiagInfoIntPtr64 = 0;
		DiagInfoIntPtr = 0;
		#ifdef _LP64 // sushil
		returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,0,SQL_DIAG_ROW_COUNT,(SQLSMALLINT *)&DiagInfoIntPtr64,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
		#else
		returncode = SQLGetDiagField(SQL_HANDLE_STMT,hstmt,0,SQL_DIAG_ROW_COUNT,(SQLSMALLINT *)&DiagInfoIntPtr,sizeof(DiagInfoIntPtr),(SQLSMALLINT *)&StringLengthPtr);
		#endif
	    if(DiagInfoIntPtr != 0)
		   DiagInfoIntPtr64 = DiagInfoIntPtr;

		if ((returncode != SQL_SUCCESS) && (returncode != SQL_SUCCESS_WITH_INFO))	
		TEST_FAILED;

		if ( i == 6 )
        {  if (DiagInfoIntPtr64 != 0)
				{
				LogMsg(ERRMSG, _T("SQLGetDiagField for SQL_DIAG_ROW_COUNT: DiagInfoIntPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), 0, DiagInfoIntPtr,__LINE__);
				TEST_FAILED;
				}
		}
		else if ( i == 4 || i == 5 )
		{ if (DiagInfoIntPtr64 != 3)
	   		{
			LogMsg(ERRMSG, _T("SQLGetDiagField for SQL_DIAG_ROW_COUNT: DiagInfoIntPtr value mismatched - Expected: %d and actual: %d , line = %d\n"), 3, DiagInfoIntPtr,__LINE__);
			TEST_FAILED;
			}
		}
    	else	
		{	if (DiagInfoIntPtr64 != 1)
		 		{
				LogMsg(ERRMSG, _T("SQLGetDiagField for SQL_DIAG_ROW_COUNT: DiagInfoIntPtr value mismatched - Expected: %d and actual: %d, line = %d \n"), 1, DiagInfoIntPtr,__LINE__);
				TEST_FAILED;
				}
		}
	}


//========================================================================================================

	//SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[4],SQL_NTS); /* CLEANUP */
	free(DiagInfoCharPtr);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLGetDiagField\n"));
	FullDisconnect3(pTestInfo);
	free_list(var_list);
	TEST_RETURN;
}
