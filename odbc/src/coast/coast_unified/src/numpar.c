#include <stdio.h>
#include <stdlib.h>
#include <windows.h>
#include <sqlext.h>
#include <string.h>
#include "basedef.h"
#include "common.h"
#include "log.h"

/*
---------------------------------------------------------
   TestSQLNumParams
---------------------------------------------------------
*/
PassFail TestSQLNumParams(TestInfo *pTestInfo)
{                  
	TEST_DECLARE;
	TCHAR			Heading[MAX_STRING_SIZE];
	RETCODE			returncode;
 	SQLHANDLE 		henv;
 	SQLHANDLE 		hdbc;
 	SQLHANDLE		hstmt;
	SWORD			param;
	TCHAR			*ExecDirStr[] = {_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--"),_T("--")};
	TCHAR			*TestCase[] = {_T("after preparing stmt "),
									_T("after preparing & binding stmt "),
									_T("after preparing, binding & executing stmt "),
									_T("after preparing, binding, executing & fetching stmt ")};

	int				lend = 4, iend = 6;
	SQLUSMALLINT	i = 0, j = 0, k = 0, l = 0;
	int				expparam[] = {1,3,6,9,2,4};
	SQLLEN			cbIn = SQL_NTS;

//===========================================================================================================
	var_list_t *var_list;
	var_list = load_api_vars(_T("SQLNumparams"), charset_file);
	if (var_list == NULL) return FAILED;

	ExecDirStr[0] = var_mapping(_T("SQLNumParams_ExecDirStr_0"), var_list);
	ExecDirStr[1] = var_mapping(_T("SQLNumParams_ExecDirStr_1"), var_list);
	ExecDirStr[2] = var_mapping(_T("SQLNumParams_ExecDirStr_2"), var_list);
	ExecDirStr[3] = var_mapping(_T("SQLNumParams_ExecDirStr_3"), var_list);
	ExecDirStr[4] = var_mapping(_T("SQLNumParams_ExecDirStr_4"), var_list);
	ExecDirStr[5] = var_mapping(_T("SQLNumParams_ExecDirStr_5"), var_list);
	ExecDirStr[6] = var_mapping(_T("SQLNumParams_ExecDirStr_6"), var_list);
	ExecDirStr[7] = var_mapping(_T("SQLNumParams_ExecDirStr_7"), var_list);
	ExecDirStr[8] = var_mapping(_T("SQLNumParams_ExecDirStr_8"), var_list);
	ExecDirStr[9] = var_mapping(_T("SQLNumParams_ExecDirStr_9"), var_list);
	ExecDirStr[10] = var_mapping(_T("SQLNumParams_ExecDirStr_10"), var_list);
	ExecDirStr[11] = var_mapping(_T("SQLNumParams_ExecDirStr_11"), var_list);
	ExecDirStr[12] = var_mapping(_T("SQLNumParams_ExecDirStr_12"), var_list);
	ExecDirStr[13] = var_mapping(_T("SQLNumParams_ExecDirStr_13"), var_list);
	ExecDirStr[14] = var_mapping(_T("SQLNumParams_ExecDirStr_14"), var_list);
	ExecDirStr[15] = var_mapping(_T("SQLNumParams_ExecDirStr_15"), var_list);
	ExecDirStr[16] = var_mapping(_T("SQLNumParams_ExecDirStr_16"), var_list);
	ExecDirStr[17] = var_mapping(_T("SQLNumParams_ExecDirStr_17"), var_list);
	ExecDirStr[18] = var_mapping(_T("SQLNumParams_ExecDirStr_18"), var_list);
	ExecDirStr[19] = var_mapping(_T("SQLNumParams_ExecDirStr_19"), var_list);

//===========================================================================================================

	LogMsg(LINEBEFORE+SHORTTIMESTAMP,_T("Begin testing API =>SQLNumParams.\n"));

	TEST_INIT;
	   
  returncode=FullConnect(pTestInfo);
  if (pTestInfo->hdbc == (SQLHANDLE)NULL)
	{
		TEST_FAILED;
		TEST_RETURN;
	}

	henv = pTestInfo->henv;
 	hdbc = pTestInfo->hdbc;
 	hstmt = (SQLHANDLE)pTestInfo->hstmt;
   	
	returncode = SQLAllocStmt((SQLHANDLE)hdbc, &hstmt);	
	if (returncode == SQL_SUCCESS)
	{
		for (l = 0; l < lend; l++)
		{
			for (i = 0; i < iend; i++)
			{
				//==================================================================================
				SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[i],SQL_NTS); /* cleanup */
				returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[i+iend],SQL_NTS);
				if ((returncode == SQL_SUCCESS) && (i > 3))
					returncode = SQLExecDirect(hstmt,(SQLTCHAR*)ExecDirStr[i+iend+iend+2],SQL_NTS);
				if (returncode == SQL_SUCCESS)
				{
					_stprintf(Heading,_T("Test Positive Functionality of SQLNumParams "));
					_tcscat(Heading, TestCase[l]);
					_tcscat(Heading, ExecDirStr[i+iend+iend]);
					_tcscat(Heading, _T("\n"));
					TESTCASE_BEGINW(Heading);
					returncode = SQLPrepare(hstmt,(SQLTCHAR*)ExecDirStr[i+iend+iend], SQL_NTS);
					if (returncode == SQL_SUCCESS || returncode == SQL_SUCCESS_WITH_INFO)
					{
						if (returncode == SQL_SUCCESS_WITH_INFO) 
							LogAllErrors(henv,hdbc,hstmt);
						if ( l == 1)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_TCHAR,SQL_INTEGER,0,0,(SQLPOINTER)_T("10"),300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQL_SUCCESS;
							else
								returncode = SQL_ERROR;
						}
						else if (l == 2)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_TCHAR,SQL_INTEGER,0,0,(SQLPOINTER)_T("10"),300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQLExecute(hstmt);
							else
								returncode = SQL_ERROR;
						}
						else if (l == 3)
						{
							for (j = 0, k = 0; j < expparam[i]; j++)
							{
								returncode = SQLBindParameter(hstmt,(SWORD)(j+1),SQL_PARAM_INPUT,SQL_C_TCHAR,SQL_INTEGER,0,0,(SQLPOINTER)_T("10"),300,&cbIn);
								if (returncode == SQL_SUCCESS)
									k++;
							}
							if (k == j)
								returncode = SQLExecute(hstmt);
								if ((returncode == SQL_SUCCESS) && (i > 3))
									returncode = SQLFetch(hstmt);
						} 
						else
							returncode = SQL_SUCCESS;
						if (returncode == SQL_SUCCESS)
						{
							returncode = SQLNumParams(hstmt, &param);
							if(!CHECKRC(SQL_SUCCESS,returncode,"SQLNumParams"))
							{
								TEST_FAILED;
								LogAllErrors(henv,hdbc,hstmt);
							}
							if (param == expparam[i])
							{
								LogMsg(NONE,_T("expect: %d and actual: %d are matched\n"),expparam[i], param);
								TESTCASE_END;
							}	
							else
							{
								TEST_FAILED;	
								LogMsg(NONE,_T("expect: %d and actual: %d are not matched\n"),expparam[i], param);
							}
						}
						else
						{
							TEST_FAILED;
							LogAllErrors(henv,hdbc,hstmt);
						}
					}
					else
					{
						TEST_FAILED;
						LogAllErrors(henv,hdbc,hstmt);
					}
				}
				else
				{
					TEST_FAILED;
					LogAllErrors(henv,hdbc,hstmt);
				}
				SQLFreeStmt(hstmt,SQL_CLOSE);
				SQLExecDirect(hstmt,(SQLTCHAR*) ExecDirStr[i],SQL_NTS); /* cleanup */
				//==================================================================================
			} /* for i loop */
		} /* for l loop */
	}

	FullDisconnect(pTestInfo);
	LogMsg(SHORTTIMESTAMP+LINEAFTER,_T("End testing API => SQLNumParams.\n"));
	free_list(var_list);
	TEST_RETURN;
}
