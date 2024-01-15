"use strict";
(self["webpackChunk_datalayer_jupyter_iam"] = self["webpackChunk_datalayer_jupyter_iam"] || []).push([["lib_index_js"],{

/***/ "./lib/auth/index.js":
/*!***************************!*\
  !*** ./lib/auth/index.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getStoredToken": () => (/* reexport safe */ _AuthStorage__WEBPACK_IMPORTED_MODULE_0__.getStoredToken),
/* harmony export */   "getStoredUser": () => (/* reexport safe */ _AuthStorage__WEBPACK_IMPORTED_MODULE_0__.getStoredUser),
/* harmony export */   "storeToken": () => (/* reexport safe */ _AuthStorage__WEBPACK_IMPORTED_MODULE_0__.storeToken),
/* harmony export */   "storeUser": () => (/* reexport safe */ _AuthStorage__WEBPACK_IMPORTED_MODULE_0__.storeUser)
/* harmony export */ });
/* harmony import */ var _AuthStorage__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./AuthStorage */ "./lib/auth/AuthStorage.js");



/***/ }),

/***/ "./lib/components/backdrop/Backdrop.js":
/*!*********************************************!*\
  !*** ./lib/components/backdrop/Backdrop.js ***!
  \*********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! styled-components */ "webpack/sharing/consume/default/styled-components/styled-components?16a2");
/* harmony import */ var styled_components__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(styled_components__WEBPACK_IMPORTED_MODULE_1__);


const BackdropComponent = (styled_components__WEBPACK_IMPORTED_MODULE_1___default().div) `
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(0, 0, 0, 0.3);
  height: 100vh;
  width: 100vw;
  right: 0;
  top: 0;
  z-index: 1000000000;
`;
function Backdrop({ open, element }) {
    return open ? (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(BackdropComponent, { children: element }) : (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {});
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Backdrop);


/***/ }),

/***/ "./lib/config/IAMConfig.js":
/*!*********************************!*\
  !*** ./lib/config/IAMConfig.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getIamServer": () => (/* binding */ getIamServer),
/* harmony export */   "loadIAMConfig": () => (/* binding */ loadIAMConfig),
/* harmony export */   "setIamServer": () => (/* binding */ setIamServer)
/* harmony export */ });
const config = {
    iamServer: 'https://dev1.datalayer.tech',
};
const setIamServer = (iamServer) => {
    config.iamServer = iamServer;
};
const getIamServer = () => config.iamServer;
const loadIAMConfig = () => {
    let config = Object.create({});
    const htmlConfig = document.getElementById('datalayer-config-data');
    if (htmlConfig) {
        config = JSON.parse(htmlConfig.textContent || '');
        if (config['iamServer']) {
            setIamServer(config['iamServer']);
        }
    }
    return config;
};


/***/ }),

/***/ "./lib/config/index.js":
/*!*****************************!*\
  !*** ./lib/config/index.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "getIamServer": () => (/* reexport safe */ _IAMConfig__WEBPACK_IMPORTED_MODULE_0__.getIamServer),
/* harmony export */   "loadIAMConfig": () => (/* reexport safe */ _IAMConfig__WEBPACK_IMPORTED_MODULE_0__.loadIAMConfig),
/* harmony export */   "setIamServer": () => (/* reexport safe */ _IAMConfig__WEBPACK_IMPORTED_MODULE_0__.setIamServer)
/* harmony export */ });
/* harmony import */ var _IAMConfig__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./IAMConfig */ "./lib/config/IAMConfig.js");



/***/ }),

/***/ "./lib/hooks/ApiHook.js":
/*!******************************!*\
  !*** ./lib/hooks/ApiHook.js ***!
  \******************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "useApi": () => (/* binding */ useApi)
/* harmony export */ });
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils */ "./lib/utils/Name.js");
/* harmony import */ var _state__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../state */ "./lib/state/index.js");




const USERS_CACHE = new Map();
const useApi = () => {
    const { setAuth, token } = (0,_state__WEBPACK_IMPORTED_MODULE_0__.useStore)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_1__.useNavigate)();
    const apiRequest = (req) => {
        return fetch(req.url, {
            method: req.method,
            headers: {
                Accept: 'application/json',
                'Content-Type': 'application/json',
                Authorization: `Bearer ${req.token ?? token}`
            },
            body: req.body ? JSON.stringify(req.body) : undefined,
            credentials: 'include'
        })
            .then(resp => {
            if (resp.status !== 200) {
                if (resp.status === 401) {
                    setAuth(undefined, undefined);
                    navigate('/run/login');
                }
                else {
                    throw new Error(resp.status.toString());
                }
            }
            return resp.json();
        })
            .catch(error => {
            throw error;
        });
    };
    // Extension -----------------------------------------------------------------
    // User -------------------------------------------------------------------
    const me = (token) => {
        apiRequest({
            url: `${(0,_config__WEBPACK_IMPORTED_MODULE_2__.getIamServer)()}/api/iam/me`,
            method: 'GET',
            token
        }).then(resp => {
            const me = resp.me;
            if (me) {
                const user = {
                    uid: me.uid,
                    handle: me.handle,
                    email: me.email,
                    firstName: me.first_name,
                    lastName: me.last_name,
                    displayName: me.display_name,
                    joinDate: undefined
                };
                USERS_CACHE.set(user.handle, user);
                setAuth(user, token);
            }
        });
    };
    const refreshUser = (accountHandle) => {
        return apiRequest({
            url: `${(0,_config__WEBPACK_IMPORTED_MODULE_2__.getIamServer)()}/api/iam/account/${accountHandle}`,
            method: 'GET'
        }).then(resp => {
            if (resp.success) {
                if (resp.user) {
                    toUser(resp.user, USERS_CACHE);
                }
            }
            return resp;
        });
    };
    const getUser = (accountHandle) => USERS_CACHE.get(accountHandle);
    const toUser = (u, cache) => {
        if (u) {
            const user = {
                uid: u.uid,
                handle: u.user_handle_s,
                email: u.user_email_s,
                firstName: u.user_first_name_t,
                lastName: u.user_last_name_t,
                displayName: (0,_utils__WEBPACK_IMPORTED_MODULE_3__.asDisplayName)(u.user_first_name_t, u.user_last_name_t),
                joinDate: u.join_ts_dt ? new Date(u.join_ts_dt) : undefined
            };
            if (cache) {
                cache.set(user.handle, user);
            }
            return user;
        }
    };
    // --------------------------------------------------------------------------
    return {
        apiRequest,
        getUser,
        me,
        refreshUser,
    };
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (useApi);


/***/ }),

/***/ "./lib/hooks/BackdropHook.js":
/*!***********************************!*\
  !*** ./lib/hooks/BackdropHook.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BackdropProvider": () => (/* binding */ BackdropProvider),
/* harmony export */   "useBackdrop": () => (/* binding */ useBackdrop)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _components_backdrop_Backdrop__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../components/backdrop/Backdrop */ "./lib/components/backdrop/Backdrop.js");



const BackdropContext = (0,react__WEBPACK_IMPORTED_MODULE_1__.createContext)({
    openBackdrop: (element) => {
        /* no-op */
    },
    closeBackdrop: () => {
        /* no-op */
    }
});
const BackdropProvider = ({ children }) => {
    const [opened, setOpened] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [element, setElement] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)();
    const openBackdrop = (element) => {
        setElement(element);
        setOpened(true);
    };
    const closeBackdrop = () => {
        setElement(undefined);
        setOpened(false);
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(BackdropContext.Provider, { value: {
            openBackdrop: openBackdrop,
            closeBackdrop: closeBackdrop
        }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_components_backdrop_Backdrop__WEBPACK_IMPORTED_MODULE_2__["default"], { open: opened, element: element }), children] }));
};
function useBackdrop() {
    return (0,react__WEBPACK_IMPORTED_MODULE_1__.useContext)(BackdropContext);
}



/***/ }),

/***/ "./lib/hooks/NavigateHook.js":
/*!***********************************!*\
  !*** ./lib/hooks/NavigateHook.js ***!
  \***********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "useNavigate": () => (/* binding */ useNavigate)
/* harmony export */ });
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-router-dom */ "webpack/sharing/consume/default/react-router-dom/react-router-dom");
/* harmony import */ var react_router_dom__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_router_dom__WEBPACK_IMPORTED_MODULE_0__);

const useNavigate = () => {
    const routerNavigate = (0,react_router_dom__WEBPACK_IMPORTED_MODULE_0__.useNavigate)();
    const navigate = (location, e = null, resetPortals = true) => {
        if (e) {
            e.preventDefault();
        }
        window.scrollTo(0, 0);
        document.body.scrollTop = 0;
        routerNavigate(location);
    };
    return navigate;
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (useNavigate);


/***/ }),

/***/ "./lib/hooks/ToastHook.js":
/*!********************************!*\
  !*** ./lib/hooks/ToastHook.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__),
/* harmony export */   "useToast": () => (/* binding */ useToast)
/* harmony export */ });
/* harmony import */ var react_toastify__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react-toastify */ "webpack/sharing/consume/default/react-toastify/react-toastify");
/* harmony import */ var react_toastify__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react_toastify__WEBPACK_IMPORTED_MODULE_0__);

const position = react_toastify__WEBPACK_IMPORTED_MODULE_0__.toast.POSITION.TOP_CENTER;
const useToast = () => {
    const enqueueToast = (message, variant) => {
        switch (variant.variant) {
            case 'info': {
                react_toastify__WEBPACK_IMPORTED_MODULE_0__.toast.info(message, { position });
                break;
            }
            case 'success': {
                react_toastify__WEBPACK_IMPORTED_MODULE_0__.toast.success(message, { position });
                break;
            }
            case 'warning': {
                react_toastify__WEBPACK_IMPORTED_MODULE_0__.toast.warning(message, { position });
                break;
            }
            case 'error': {
                react_toastify__WEBPACK_IMPORTED_MODULE_0__.toast.error(message, { position });
                break;
            }
        }
    };
    return { enqueueToast };
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (useToast);


/***/ }),

/***/ "./lib/hooks/index.js":
/*!****************************!*\
  !*** ./lib/hooks/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "BackdropProvider": () => (/* reexport safe */ _BackdropHook__WEBPACK_IMPORTED_MODULE_1__.BackdropProvider),
/* harmony export */   "useApi": () => (/* reexport safe */ _ApiHook__WEBPACK_IMPORTED_MODULE_0__.useApi),
/* harmony export */   "useBackdrop": () => (/* reexport safe */ _BackdropHook__WEBPACK_IMPORTED_MODULE_1__.useBackdrop),
/* harmony export */   "useNavigate": () => (/* reexport safe */ _NavigateHook__WEBPACK_IMPORTED_MODULE_2__.useNavigate),
/* harmony export */   "useToast": () => (/* reexport safe */ _ToastHook__WEBPACK_IMPORTED_MODULE_3__.useToast)
/* harmony export */ });
/* harmony import */ var _ApiHook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./ApiHook */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _BackdropHook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./BackdropHook */ "./lib/hooks/BackdropHook.js");
/* harmony import */ var _NavigateHook__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./NavigateHook */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _ToastHook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./ToastHook */ "./lib/hooks/ToastHook.js");






/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ANONYMOUS_TOKEN": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_4__.ANONYMOUS_TOKEN),
/* harmony export */   "ANONYMOUS_USER": () => (/* reexport safe */ _model__WEBPACK_IMPORTED_MODULE_4__.ANONYMOUS_USER),
/* harmony export */   "BackdropProvider": () => (/* reexport safe */ _hooks__WEBPACK_IMPORTED_MODULE_2__.BackdropProvider),
/* harmony export */   "IJupyterIAM": () => (/* reexport safe */ _jupyterlab__WEBPACK_IMPORTED_MODULE_3__.IJupyterIAM),
/* harmony export */   "JoinConfirm": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.JoinConfirm),
/* harmony export */   "JoinForm": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.JoinForm),
/* harmony export */   "JoinWelcome": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.JoinWelcome),
/* harmony export */   "LoginForm": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.LoginForm),
/* harmony export */   "Logout": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.Logout),
/* harmony export */   "NewPasswordConfirm": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.NewPasswordConfirm),
/* harmony export */   "NewPasswordForm": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.NewPasswordForm),
/* harmony export */   "NewPasswordWelcome": () => (/* reexport safe */ _views_auth__WEBPACK_IMPORTED_MODULE_6__.NewPasswordWelcome),
/* harmony export */   "getIamServer": () => (/* reexport safe */ _config__WEBPACK_IMPORTED_MODULE_1__.getIamServer),
/* harmony export */   "getStoredToken": () => (/* reexport safe */ _auth__WEBPACK_IMPORTED_MODULE_0__.getStoredToken),
/* harmony export */   "getStoredUser": () => (/* reexport safe */ _auth__WEBPACK_IMPORTED_MODULE_0__.getStoredUser),
/* harmony export */   "loadIAMConfig": () => (/* reexport safe */ _config__WEBPACK_IMPORTED_MODULE_1__.loadIAMConfig),
/* harmony export */   "setIamServer": () => (/* reexport safe */ _config__WEBPACK_IMPORTED_MODULE_1__.setIamServer),
/* harmony export */   "storeToken": () => (/* reexport safe */ _auth__WEBPACK_IMPORTED_MODULE_0__.storeToken),
/* harmony export */   "storeUser": () => (/* reexport safe */ _auth__WEBPACK_IMPORTED_MODULE_0__.storeUser),
/* harmony export */   "useApi": () => (/* reexport safe */ _hooks__WEBPACK_IMPORTED_MODULE_2__.useApi),
/* harmony export */   "useBackdrop": () => (/* reexport safe */ _hooks__WEBPACK_IMPORTED_MODULE_2__.useBackdrop),
/* harmony export */   "useNavigate": () => (/* reexport safe */ _hooks__WEBPACK_IMPORTED_MODULE_2__.useNavigate),
/* harmony export */   "useStore": () => (/* reexport safe */ _state__WEBPACK_IMPORTED_MODULE_5__.useStore),
/* harmony export */   "useToast": () => (/* reexport safe */ _hooks__WEBPACK_IMPORTED_MODULE_2__.useToast)
/* harmony export */ });
/* harmony import */ var _auth__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./auth */ "./lib/auth/index.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./config */ "./lib/config/index.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./hooks */ "./lib/hooks/index.js");
/* harmony import */ var _jupyterlab__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./jupyterlab */ "./lib/jupyterlab/index.js");
/* harmony import */ var _model__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./model */ "./lib/model/index.js");
/* harmony import */ var _state__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./state */ "./lib/state/index.js");
/* harmony import */ var _views_auth__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./views/auth */ "./lib/views/auth/index.js");










/***/ }),

/***/ "./lib/model/index.js":
/*!****************************!*\
  !*** ./lib/model/index.js ***!
  \****************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ANONYMOUS_TOKEN": () => (/* reexport safe */ _User__WEBPACK_IMPORTED_MODULE_0__.ANONYMOUS_TOKEN),
/* harmony export */   "ANONYMOUS_USER": () => (/* reexport safe */ _User__WEBPACK_IMPORTED_MODULE_0__.ANONYMOUS_USER)
/* harmony export */ });
/* harmony import */ var _User__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./User */ "./lib/model/User.js");



/***/ }),

/***/ "./lib/utils/Name.js":
/*!***************************!*\
  !*** ./lib/utils/Name.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "asDisplayName": () => (/* binding */ asDisplayName),
/* harmony export */   "asInitials": () => (/* binding */ asInitials)
/* harmony export */ });
const asDisplayName = (firstName, lastName) => {
    return firstName
        ? lastName
            ? firstName + ' ' + lastName
            : firstName
        : lastName ?? '';
};
const asInitials = (name) => name
    .replace(/\s+/, ' ')
    .split(' ')
    .slice(0, 2)
    .map(v => v && v[0].toUpperCase())
    .join('');


/***/ }),

/***/ "./lib/utils/Validator.js":
/*!********************************!*\
  !*** ./lib/utils/Validator.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "validateEmail": () => (/* binding */ validateEmail),
/* harmony export */   "validateLength": () => (/* binding */ validateLength)
/* harmony export */ });
const EMAIL_REX = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
const validateEmail = (value) => {
    if (EMAIL_REX.test(value)) {
        return true;
    }
    return false;
};
/**
 * Verify if a string has a given length or not.
 */
const validateLength = (value, minLength) => {
    if (value.length >= minLength) {
        return true;
    }
    return false;
};


/***/ }),

/***/ "./lib/views/auth/JoinConfirm.js":
/*!***************************************!*\
  !*** ./lib/views/auth/JoinConfirm.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JoinConfirm": () => (/* binding */ JoinConfirm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react-brand */ "../../../node_modules/@primer/react-brand/lib/index.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../utils */ "./lib/utils/Validator.js");







const JoinConfirm = (props) => {
    const { loginRoute, joinWelcomeRoute } = props;
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useNavigate)();
    const { apiRequest } = (0,_hooks__WEBPACK_IMPORTED_MODULE_4__.useApi)();
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_5__.useToast)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [formValues, setFormValues] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        token: undefined
    });
    const [validationResult, setValidationResult] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        token: undefined
    });
    const handleHandleChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            handle: event.target.value
        }));
    };
    const handleTokenChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            token: event.target.value
        }));
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setValidationResult({
            ...validationResult,
            handle: formValues.handle === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.handle, 1)
                    ? 'success'
                    : 'error',
            token: formValues.token === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.token, 1)
                    ? 'success'
                    : 'error'
        });
    }, [formValues]);
    const validateForm = (data) => {
        return true;
    };
    const submit = async () => {
        if (loading) {
            return;
        }
        if (validateForm(formValues)) {
            setLoading(true);
            apiRequest({
                url: `${(0,_config__WEBPACK_IMPORTED_MODULE_7__.getIamServer)()}/api/iam/join/confirm/${formValues.handle}/${formValues.token}`,
                method: 'GET'
            })
                .then(resp => {
                if (resp.success) {
                    navigate(joinWelcomeRoute);
                }
                else {
                    enqueueToast(resp.message, { variant: 'error' });
                }
            })
                .catch(err => {
                console.error(err);
                enqueueToast('Application Error.', { variant: 'error' });
                navigate(loginRoute);
            });
        }
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { colorMode: "light", style: { backgroundColor: 'var(--brand-color-canvas-default)' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { style: { height: 'calc(100vh - 250px)' }, pl: 5, pr: 5, pt: 10, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { maxWidth: '1280px', margin: '0 auto' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Heading, { children: "Activate Datalayer" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { display: "grid", gridTemplateColumns: "1fr 1fr", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { label: { marginTop: 2 } }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.handle, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your handle" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { autoFocus: true, fullWidth: true, value: formValues.handle, onChange: handleHandleChange }), validationResult.handle === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your handle must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.token, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your activation code (check your mail)" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "email", value: formValues.token, onChange: handleTokenChange }), validationResult.token === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your activation code is too small." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { display: 'flex' }, mt: 2, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Button, { variant: "primary", type: "submit", disabled: loading ||
                                                    validationResult.handle !== 'success' ||
                                                    validationResult.token !== 'success', onClick: submit, children: loading ? 'Activating...' : 'Activate' }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { m: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.CTABanner, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("span", {}) }) })] })] }) }) }) }));
};
JoinConfirm.defaultProps = {
    loginRoute: '/jupyter/kernels/login',
    joinWelcomeRoute: '/jupyter/kernels/join/welcome',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JoinConfirm);


/***/ }),

/***/ "./lib/views/auth/JoinForm.js":
/*!************************************!*\
  !*** ./lib/views/auth/JoinForm.js ***!
  \************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JoinForm": () => (/* binding */ JoinForm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react-brand */ "../../../node_modules/@primer/react-brand/lib/index.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../utils */ "./lib/utils/Validator.js");







const JoinForm = (props) => {
    const { joinConfirmRoute } = props;
    const { apiRequest } = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useApi)();
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_4__.useToast)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_5__.useNavigate)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [formValues, setFormValues] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        email: undefined,
        firstName: undefined,
        lastName: undefined,
        password: undefined,
        passwordConfirm: undefined
        //    terms: undefined,
    });
    const [validationResult, setValidationResult] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        email: undefined,
        firstName: undefined,
        lastName: undefined,
        password: undefined,
        passwordConfirm: undefined
        //    terms: undefined,
    });
    const handleHandleChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            handle: event.target.value
        }));
    };
    const handleEmailChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            email: event.target.value
        }));
    };
    const handleFirstNameChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            firstName: event.target.value
        }));
    };
    const handleLastNameChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            lastName: event.target.value
        }));
    };
    const handlePasswordChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            password: event.target.value
        }));
    };
    const handlePasswordConfirmChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            passwordConfirm: event.target.value
        }));
    };
    /*
    const handleTermsChange = (event: React.ChangeEvent<any>) => {
      setFormValues((prevFormValues) => ({
        ...prevFormValues,
        terms: event.target.checked,
      }));
    };
    */
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setValidationResult({
            ...validationResult,
            handle: formValues.handle === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.handle, 1)
                    ? 'success'
                    : 'error',
            email: formValues.email === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateEmail)(formValues.email)
                    ? 'success'
                    : 'error',
            firstName: formValues.firstName === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.firstName, 1)
                    ? 'success'
                    : 'error',
            lastName: formValues.lastName === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.lastName, 1)
                    ? 'success'
                    : 'error',
            password: formValues.password === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.password, 5)
                    ? 'success'
                    : 'error',
            passwordConfirm: formValues.passwordConfirm === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.passwordConfirm, 5)
                    ? 'success'
                    : 'error'
            //      terms: formValues.passwordConfirm === undefined ? undefined : formValues.terms ? "success" : "error",
        });
    }, [formValues]);
    const validateForm = (data) => {
        if (data.password !== data.passwordConfirm) {
            enqueueToast('Please make sure your passwords match.', {
                variant: 'warning'
            });
            return false;
        }
        return true;
    };
    const submit = async () => {
        if (loading) {
            return;
        }
        if (validateForm(formValues)) {
            setLoading(true);
            apiRequest({
                url: `${(0,_config__WEBPACK_IMPORTED_MODULE_7__.getIamServer)()}/api/iam/join/request/token`,
                method: 'POST',
                body: {
                    handle: formValues.handle,
                    email: formValues.email,
                    firstName: formValues.firstName,
                    lastName: formValues.lastName,
                    password: formValues.password,
                    passwordConfirm: formValues.passwordConfirm
                }
            })
                .then(resp => {
                setLoading(false);
                if (resp.success) {
                    enqueueToast(resp.message, { variant: 'success' });
                    navigate(joinConfirmRoute);
                }
                else {
                    enqueueToast(resp.message, { variant: 'warning' });
                    resp.errors.map((error) => enqueueToast(error, { variant: 'error' }));
                }
            })
                .catch(err => {
                console.error(err);
                setLoading(false);
                enqueueToast('Application Error.', { variant: 'error' });
            });
        }
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { colorMode: "light", style: { backgroundColor: 'var(--brand-color-canvas-default)' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { style: { height: 'calc(100vh - 250px)' }, pl: 5, pr: 5, pt: 10, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { maxWidth: '1280px', margin: '0 auto' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Heading, { children: "Join Datalayer" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { display: "grid", gridTemplateColumns: "1fr 1fr", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { label: { marginTop: 2 } }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.handle, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your handle" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { autoFocus: true, fullWidth: true, value: formValues.handle, onChange: handleHandleChange }), validationResult.handle === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your handle must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.email, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your email" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "email", value: formValues.email, onChange: handleEmailChange }), validationResult.email === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your email is not valid." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.firstName, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your first name" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, value: formValues.firstName, onChange: handleFirstNameChange }), validationResult.firstName === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your first name must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.lastName, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your last name" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, value: formValues.lastName, onChange: handleLastNameChange }), validationResult.lastName === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your last name must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.password, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your password" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "password", value: formValues.password, onChange: handlePasswordChange }), validationResult.password === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your password is not valid." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.passwordConfirm, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your password confirmation" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "password", value: formValues.passwordConfirm, onChange: handlePasswordConfirmChange }), validationResult.passwordConfirm === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your password confirmation is not valid." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { display: 'flex' }, mt: 2, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Button, { variant: "primary", type: "submit", disabled: loading ||
                                                    validationResult.handle !== 'success' ||
                                                    validationResult.email !== 'success' ||
                                                    validationResult.firstName !== 'success' ||
                                                    validationResult.lastName !== 'success' ||
                                                    validationResult.password !== 'success' ||
                                                    validationResult.passwordConfirm !== 'success', onClick: submit, children: loading ? 'Requesting...' : 'Request to join' }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { m: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.CTABanner, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("span", {}) }) })] })] }) }) }) }));
};
JoinForm.defaultProps = {
    joinConfirmRoute: '/jupyter/kernels/join/confirm',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JoinForm);


/***/ }),

/***/ "./lib/views/auth/JoinWelcome.js":
/*!***************************************!*\
  !*** ./lib/views/auth/JoinWelcome.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JoinWelcome": () => (/* binding */ JoinWelcome),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../hooks */ "./lib/hooks/NavigateHook.js");



const JoinWelcome = (props) => {
    const { loginRoute } = props;
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_2__.useToast)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useNavigate)();
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        enqueueToast('Welcome to Datalayer - Login with your username and password', { variant: 'success' });
        navigate(loginRoute);
    }, []);
    return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {});
};
JoinWelcome.defaultProps = {
    loginRoute: '/jupyter/kernels/login',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (JoinWelcome);


/***/ }),

/***/ "./lib/views/auth/LoginForm.js":
/*!*************************************!*\
  !*** ./lib/views/auth/LoginForm.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "LoginForm": () => (/* binding */ LoginForm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react-brand */ "../../../node_modules/@primer/react-brand/lib/index.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./../../utils */ "./lib/utils/Name.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./../../utils */ "./lib/utils/Validator.js");
/* harmony import */ var _state__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../state */ "./lib/state/index.js");








const LoginForm = (props) => {
    const { homeRoute, joinRoute, passwordRoute, joinConfirmRoute } = props;
    const { apiRequest } = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useApi)();
    const { setAuth } = (0,_state__WEBPACK_IMPORTED_MODULE_4__["default"])();
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_5__.useToast)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_6__.useNavigate)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [formValues, setFormValues] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        password: undefined
    });
    const [validationResult, setValidationResult] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        password: undefined
    });
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            submit();
        }
    };
    const handleHandleChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            handle: event.target.value
        }));
    };
    const handlePasswordChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            password: event.target.value
        }));
    };
    const submit = async () => {
        if (loading || !validationResult.handle || !validationResult.password) {
            return;
        }
        setLoading(true);
        apiRequest({
            url: `${(0,_config__WEBPACK_IMPORTED_MODULE_7__.getIamServer)()}/api/iam/login`,
            method: 'POST',
            body: {
                handle: formValues.handle,
                password: formValues.password
            }
        })
            .then(resp => {
            setLoading(false);
            if (resp.success) {
                const token = resp.token;
                const user = {
                    handle: resp.user.user_handle_s,
                    firstName: resp.user.user_first_name_t,
                    lastName: resp.user.user_last_name_t,
                    displayName: (0,_utils__WEBPACK_IMPORTED_MODULE_8__.asDisplayName)(resp.user.user_first_name_t, resp.user.user_last_name_t),
                    credits: resp.user.credits_i,
                    joinDate: resp.user.join_ts_dt
                        ? new Date(resp.user.join_ts_dt)
                        : undefined,
                    email: resp.user.user_email_s
                };
                setAuth(user, token);
                navigate(homeRoute);
            }
            else {
                enqueueToast(resp.message, { variant: 'warning' });
                if (resp.errors) {
                    resp.errors.map((error) => enqueueToast(error, { variant: 'warning' }));
                }
            }
        })
            .catch(err => {
            console.error(err);
            setLoading(false);
            enqueueToast('Application Error.', { variant: 'error' });
        });
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setValidationResult({
            ...validationResult,
            handle: formValues.handle === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_9__.validateLength)(formValues.handle, 1)
                    ? 'success'
                    : 'error',
            password: formValues.password === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_9__.validateLength)(formValues.password, 1)
                    ? 'success'
                    : 'error'
        });
    }, [formValues]);
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { colorMode: "light", style: { backgroundColor: 'var(--brand-color-canvas-default)' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { style: { height: 'calc(100vh - 250px)' }, pl: 5, pr: 5, pt: 10, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { sx: { maxWidth: '1280px', margin: '0 auto' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Heading, { children: "Login to Datalayer" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { display: "grid", gridTemplateColumns: "1fr 1fr", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { sx: { label: { marginTop: 2 }, paddingRight: '10%' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { mt: 5, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.handle, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your handle" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { autoFocus: true, fullWidth: true, placeholder: "Your handle", size: "large", value: formValues.handle, onChange: handleHandleChange, onKeyDown: handleKeyDown }), validationResult.handle === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your handle may not be empty." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.password, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your password" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, placeholder: "Your password", size: "large", type: "password", value: formValues.password, onChange: handlePasswordChange, onKeyDown: handleKeyDown }), validationResult.password === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your password may not be empty." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { mt: 5, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Button, { variant: "primary", disabled: loading ||
                                                        validationResult.handle !== 'success' ||
                                                        validationResult.password !== 'success', onClick: submit, children: loading ? 'Login...' : 'Login' }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { pt: 6 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Link, { onClick: () => {
                                                        navigate(joinRoute);
                                                    }, children: "Don't have an account?" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { pt: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Link, { onClick: () => {
                                                        navigate(passwordRoute);
                                                    }, children: "Forgot password?" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { pt: 3 }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Link, { onClick: () => {
                                                        navigate(joinConfirmRoute);
                                                    }, children: "Activate your account with a code" })] })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_10__["default"], { m: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.CTABanner, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("span", {}) }) })] })] }) }) }) }));
};
LoginForm.defaultProps = {
    homeRoute: '/jupyter/kernels',
    joinRoute: '/jupyter/kernels/join',
    passwordRoute: '/jupyter/kernels/password',
    joinConfirmRoute: '/jupyter/kernels/join/confirm',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (LoginForm);


/***/ }),

/***/ "./lib/views/auth/Logout.js":
/*!**********************************!*\
  !*** ./lib/views/auth/Logout.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Logout": () => (/* binding */ Logout),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _state__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../state */ "./lib/state/index.js");




const Logout = (props) => {
    const { homeRoute } = props;
    const { setAuth } = (0,_state__WEBPACK_IMPORTED_MODULE_2__["default"])();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useNavigate)();
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setAuth(undefined, undefined);
        navigate(homeRoute);
    }, []);
    return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {});
};
Logout.defaultProps = {
    homeRoute: '/jupyter/kernels',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (Logout);


/***/ }),

/***/ "./lib/views/auth/NewPasswordConfirm.js":
/*!**********************************************!*\
  !*** ./lib/views/auth/NewPasswordConfirm.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewPasswordConfirm": () => (/* binding */ NewPasswordConfirm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react-brand */ "../../../node_modules/@primer/react-brand/lib/index.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../utils */ "./lib/utils/Validator.js");







const NewPasswordConfirm = (props) => {
    const { loginRoute, passwordWelcomeRoute } = props;
    const { apiRequest } = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useApi)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_4__.useNavigate)();
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_5__.useToast)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [formValues, setFormValues] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        token: undefined
    });
    const [validationResult, setValidationResult] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        token: undefined
    });
    const handleHandleChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            handle: event.target.value
        }));
    };
    const handleTokenChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            token: event.target.value
        }));
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setValidationResult({
            ...validationResult,
            handle: formValues.handle === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.handle, 1)
                    ? 'success'
                    : 'error',
            token: formValues.token === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.token, 1)
                    ? 'success'
                    : 'error'
        });
    }, [formValues]);
    const validateForm = (data) => {
        return true;
    };
    const submit = async () => {
        if (loading) {
            return;
        }
        if (validateForm(formValues)) {
            setLoading(true);
            apiRequest({
                url: `${(0,_config__WEBPACK_IMPORTED_MODULE_7__.getIamServer)()}/api/iam/password/confirm/${formValues.handle}/${formValues.token}`,
                method: 'GET'
            })
                .then(resp => {
                if (resp.success) {
                    navigate(passwordWelcomeRoute);
                }
                else {
                    enqueueToast(resp.message, { variant: 'error' });
                    navigate(loginRoute);
                }
            })
                .catch(err => {
                console.error(err);
                enqueueToast('Application Error.', { variant: 'error' });
                navigate(loginRoute);
            });
        }
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { colorMode: "light", style: { backgroundColor: 'var(--brand-color-canvas-default)' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { style: { height: 'calc(100vh - 250px)' }, pl: 5, pr: 5, pt: 10, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { maxWidth: '1280px', margin: '0 auto' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Heading, { children: "Confirm your password" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { display: "grid", gridTemplateColumns: "1fr 1fr", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { label: { marginTop: 2 } }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.handle, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your handle" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { autoFocus: true, fullWidth: true, value: formValues.handle, onChange: handleHandleChange }), validationResult.handle === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your handle must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.token, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your activation code (check your mail)" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "email", value: formValues.token, onChange: handleTokenChange }), validationResult.token === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your activation token is too small." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { display: 'flex' }, mt: 2, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Button, { variant: "primary", type: "submit", disabled: loading ||
                                                    validationResult.handle !== 'success' ||
                                                    validationResult.token !== 'success', onClick: submit, children: loading ? 'Activating...' : 'Activate' }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { m: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.CTABanner, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("span", {}) }) })] })] }) }) }) }));
};
NewPasswordConfirm.defaultProps = {
    loginRoute: '/jupyter/kernels/login',
    passwordWelcomeRoute: '/jupyter/kernels/password/welcome',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (NewPasswordConfirm);


/***/ }),

/***/ "./lib/views/auth/NewPasswordForm.js":
/*!*******************************************!*\
  !*** ./lib/views/auth/NewPasswordForm.js ***!
  \*******************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewPasswordForm": () => (/* binding */ NewPasswordForm),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _primer_react__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @primer/react */ "../../../node_modules/@primer/react/lib-esm/Box/Box.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @primer/react-brand */ "../../../node_modules/@primer/react-brand/lib/index.js");
/* harmony import */ var _primer_react_brand__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _config__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./../../config */ "./lib/config/IAMConfig.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ApiHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../utils */ "./lib/utils/Validator.js");







const NewPasswordForm = (props) => {
    const { passwordConfirmRoute } = props;
    const { apiRequest } = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useApi)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_4__.useNavigate)();
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_5__.useToast)();
    const [loading, setLoading] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)(false);
    const [formValues, setFormValues] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        password: undefined,
        passwordConfirm: undefined
    });
    const [validationResult, setValidationResult] = (0,react__WEBPACK_IMPORTED_MODULE_1__.useState)({
        handle: undefined,
        password: undefined,
        passwordConfirm: undefined
    });
    const handleHandleChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            handle: event.target.value
        }));
    };
    const handlePasswordChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            password: event.target.value
        }));
    };
    const handlePasswordConfirmChange = (event) => {
        setFormValues(prevFormValues => ({
            ...prevFormValues,
            passwordConfirm: event.target.value
        }));
    };
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        setValidationResult({
            ...validationResult,
            handle: formValues.password === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.password, 1)
                    ? 'success'
                    : 'error',
            password: formValues.password === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.password, 5)
                    ? 'success'
                    : 'error',
            passwordConfirm: formValues.passwordConfirm === undefined
                ? undefined
                : (0,_utils__WEBPACK_IMPORTED_MODULE_6__.validateLength)(formValues.passwordConfirm, 5)
                    ? 'success'
                    : 'error'
        });
    }, [formValues]);
    const validateForm = () => {
        if (formValues.password !== formValues.passwordConfirm) {
            enqueueToast('Please make sure your passwords match.', {
                variant: 'warning'
            });
            return false;
        }
        return true;
    };
    const submit = () => {
        if (loading) {
            return;
        }
        if (validateForm()) {
            setLoading(true);
            apiRequest({
                url: `${(0,_config__WEBPACK_IMPORTED_MODULE_7__.getIamServer)()}/api/iam/password/token`,
                method: 'POST',
                body: {
                    handle: formValues.handle,
                    password: formValues.password,
                    passwordConfirm: formValues.passwordConfirm
                }
            })
                .then(resp => {
                setLoading(false);
                if (resp.success) {
                    enqueueToast(resp.message, { variant: 'success' });
                    navigate(passwordConfirmRoute);
                }
                else {
                    enqueueToast(resp.message, { variant: 'error' });
                    resp.errors.map((error) => enqueueToast(error, { variant: 'error' }));
                }
            })
                .catch(err => {
                console.error(err);
                setLoading(false);
                enqueueToast('Application Error.', { variant: 'error' });
            });
        }
    };
    return ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.ThemeProvider, { colorMode: "light", style: { backgroundColor: 'var(--brand-color-canvas-default)' }, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { style: { height: 'calc(100vh - 250px)' }, pl: 5, pr: 5, pt: 10, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { maxWidth: '1280px', margin: '0 auto' }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Heading, { children: "Change your password" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { display: "grid", gridTemplateColumns: "1fr 1fr", children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { label: { marginTop: 2 } }, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.handle, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your handle" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { autoFocus: true, fullWidth: true, value: formValues.handle, onChange: handleHandleChange }), validationResult.handle === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your handle must have more than 1 character." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.password, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your new pasword" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "password", value: formValues.password, onChange: handlePasswordChange }), validationResult.password === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your new password is not valid." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsxs)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl, { fullWidth: true, validationStatus: validationResult.passwordConfirm, children: [(0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Label, { children: "Your new password confirmation" }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.TextInput, { fullWidth: true, type: "password", value: formValues.passwordConfirm, onChange: handlePasswordConfirmChange }), validationResult.passwordConfirm === 'error' ? ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.FormControl.Validation, { children: "Your password confirmation is not valid." })) : ((0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {}))] }) }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { sx: { display: 'flex' }, mt: 2, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.Button, { variant: "primary", type: "submit", disabled: loading ||
                                                    validationResult.handle !== 'success' ||
                                                    validationResult.password !== 'success' ||
                                                    validationResult.passwordConfirm !== 'success', onClick: submit, children: loading
                                                    ? 'Sending mail to change password...'
                                                    : 'Request to change password' }) })] }), (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react__WEBPACK_IMPORTED_MODULE_8__["default"], { m: 3, children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(_primer_react_brand__WEBPACK_IMPORTED_MODULE_2__.CTABanner, { children: (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)("span", {}) }) })] })] }) }) }) }));
};
NewPasswordForm.defaultProps = {
    passwordConfirmRoute: '/jupyter/kernels/password/confirm',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (NewPasswordForm);


/***/ }),

/***/ "./lib/views/auth/NewPasswordWelcome.js":
/*!**********************************************!*\
  !*** ./lib/views/auth/NewPasswordWelcome.js ***!
  \**********************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NewPasswordWelcome": () => (/* binding */ NewPasswordWelcome),
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react/jsx-runtime */ "../../../node_modules/react/jsx-runtime.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/ToastHook.js");
/* harmony import */ var _hooks__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./../../hooks */ "./lib/hooks/NavigateHook.js");



const NewPasswordWelcome = (props) => {
    const { loginRoute } = props;
    const { enqueueToast } = (0,_hooks__WEBPACK_IMPORTED_MODULE_2__.useToast)();
    const navigate = (0,_hooks__WEBPACK_IMPORTED_MODULE_3__.useNavigate)();
    (0,react__WEBPACK_IMPORTED_MODULE_1__.useEffect)(() => {
        navigate(loginRoute);
        enqueueToast('Welcome back to Datalayer - Login with your username and new password', { variant: 'success' });
    }, []);
    return (0,react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.jsx)(react_jsx_runtime__WEBPACK_IMPORTED_MODULE_0__.Fragment, {});
};
NewPasswordWelcome.defaultProps = {
    loginRoute: '/jupyter/kernels/login',
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (NewPasswordWelcome);


/***/ }),

/***/ "./lib/views/auth/index.js":
/*!*********************************!*\
  !*** ./lib/views/auth/index.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "JoinConfirm": () => (/* reexport safe */ _JoinConfirm__WEBPACK_IMPORTED_MODULE_0__.JoinConfirm),
/* harmony export */   "JoinForm": () => (/* reexport safe */ _JoinForm__WEBPACK_IMPORTED_MODULE_1__.JoinForm),
/* harmony export */   "JoinWelcome": () => (/* reexport safe */ _JoinWelcome__WEBPACK_IMPORTED_MODULE_2__.JoinWelcome),
/* harmony export */   "LoginForm": () => (/* reexport safe */ _LoginForm__WEBPACK_IMPORTED_MODULE_3__.LoginForm),
/* harmony export */   "Logout": () => (/* reexport safe */ _Logout__WEBPACK_IMPORTED_MODULE_4__.Logout),
/* harmony export */   "NewPasswordConfirm": () => (/* reexport safe */ _NewPasswordConfirm__WEBPACK_IMPORTED_MODULE_5__.NewPasswordConfirm),
/* harmony export */   "NewPasswordForm": () => (/* reexport safe */ _NewPasswordForm__WEBPACK_IMPORTED_MODULE_6__.NewPasswordForm),
/* harmony export */   "NewPasswordWelcome": () => (/* reexport safe */ _NewPasswordWelcome__WEBPACK_IMPORTED_MODULE_7__.NewPasswordWelcome)
/* harmony export */ });
/* harmony import */ var _JoinConfirm__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./JoinConfirm */ "./lib/views/auth/JoinConfirm.js");
/* harmony import */ var _JoinForm__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./JoinForm */ "./lib/views/auth/JoinForm.js");
/* harmony import */ var _JoinWelcome__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./JoinWelcome */ "./lib/views/auth/JoinWelcome.js");
/* harmony import */ var _LoginForm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./LoginForm */ "./lib/views/auth/LoginForm.js");
/* harmony import */ var _Logout__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./Logout */ "./lib/views/auth/Logout.js");
/* harmony import */ var _NewPasswordConfirm__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./NewPasswordConfirm */ "./lib/views/auth/NewPasswordConfirm.js");
/* harmony import */ var _NewPasswordForm__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./NewPasswordForm */ "./lib/views/auth/NewPasswordForm.js");
/* harmony import */ var _NewPasswordWelcome__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./NewPasswordWelcome */ "./lib/views/auth/NewPasswordWelcome.js");











/***/ })

}]);
//# sourceMappingURL=lib_index_js.dd96e8e5c937932fc799.js.map