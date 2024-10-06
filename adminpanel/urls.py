from django.urls import path

from restaurant.views import (
    createTable, adminCreateTableView, allTablesView,
    deleteTableView, editTableView, adminEditTableView
)

from .views import (
    adminpanelHome, adminpanelOrder, deleteRolesView, deleteVendorView,
    departmentHomeView, editDepartmentView, createDepartmentView,
    createItemDepartmentView, createDepartmentCategory,
    categoryHomeView, editCategoryView, createCategoryView, createCategoryItemView, createBrand,
    editBrandView, newBrandItem, brandHomeView,
    productHomeView, editProducteView, createProducteView, deleteProductView,
    customerHomeView, editCustomerView, personalCustomerView, businessCustomerView,
    vendorView, editVendorView,createVendorView, deleteVendorView,
    employeeView,editEmployeeView,createEmployeeView,
    contactView, login_for_admin, logoutView,
    successView, failedView, notFoundView, warningView,
    # Admin
    adminDeleteCategoryiew, adminEditCategoryView,
    adminEditProductView, adminEditBrand, adminDeleteBrand, editVendorView, adminCreateBrand,
    # Contact
    submitContact,
    # Customer Edit 
    adminEditCustomerView,
    # Export
    exportCustomerData, exportProductData, exportOrderData,
    exportDueData, exportTableCheckoutData, exportAdvanceBookingData,
    # Edit logo
    adminShopLogoUpdate,
    employeeView, createEmployeeView, editEmployeeView, deleteEmployeeView,
    # Roles 
    roleViews, createRolesView, editRolesView, deleteRolesView,
    viewShopSettings, updateShopSettings,
    adminDueOrdersView, adminTableOrdersView, adminAdvancedOrdersView,
)

urlpatterns = [

    # Login For Admin of the shop owner
    path("login/", login_for_admin, name="login_for_admin"),
    # Logout For Admin of the shop owner
    path("logout/", logoutView, name="logoutView"),

    path("home/<int:shop_id>/", adminpanelHome, name="admin-home"),
    path("orders/<int:shop_id>/", adminpanelOrder, name="admin-order"),
    path("export-order-data/<int:shop_id>/", exportOrderData, name="export-order-data"),
    path("admin-edit-logo/<int:shop_id>/", adminShopLogoUpdate, name="admin-edit-logo"),

    # Department
    path("department/<int:shop_id>/", departmentHomeView, name="department"),
    path("edit-department/", editDepartmentView, name="edit-department"),
    path("create-department/", createDepartmentView, name="create-department"),
    path("create-item/", createItemDepartmentView, name="create-item"),
    path("create-department-category/", createDepartmentCategory,
         name="create-department-category"),

    # Category
    path("category/<int:shop_id>/", categoryHomeView, name="category"),
    path("edit-category/<int:shop_id>/<int:cat_id>/", editCategoryView, name="edit-category"),
    path("create-category/<int:shop_id>/", createCategoryView, name="create-category"),
    path("create-category-item/", createCategoryItemView,
         name="create-category-item"),

    # brand
    path("create-brand/<int:shop_id>/", createBrand, name="create-brand"),
    path("edit-brand/<int:shop_id>/<int:brand_id>/", editBrandView, name="edit-brand"),
    path("new-brand-item/<int:shop_id>/", newBrandItem, name="new-brand-item"),
    path("brand/<int:shop_id>/", brandHomeView, name="brand"),

    # Admin brand
    path("admin-create-brand/<int:shop_id>/", adminCreateBrand, name="admin-create-brand"),
    path("admin-edit-brand/<int:shop_id>/<int:brand_id>/", adminEditBrand, name="admin-edit-brand"),
    path("admin-delete-brand/<int:shop_id>/<int:brand_id>/", adminDeleteBrand, name="admin-delete-brand"),


    # Category form
    path("admin-delete-category/<int:shop_id>/<int:cat_id>/", adminDeleteCategoryiew, name="admin-delete-category"),
    path("admin-edit-category/<int:shop_id>/<int:cat_id>/", adminEditCategoryView, name="admin-edit-category"),

    # Product
    path("product/<int:shop_id>/", productHomeView, name="product"),
    path("edit-product/<int:shop_id>/<int:prod_id>/", editProducteView, name="edit-product"),
    path("create-product/<int:shop_id>/", createProducteView, name="create-product"),
    path("delete-product/<int:shop_id>/<int:prod_id>/", deleteProductView, name="admin-delete-product"),

    # Admin Product
    path("admin-edit-product/<int:shop_id>/<int:prod_id>/", adminEditProductView, name="admin-edit-product"),


    # customer
    path("customer/<int:shop_id>/", customerHomeView, name="customer"),
    path("edit-customer/<int:shop_id>/<int:cust_id>/", editCustomerView, name="edit-customer"),
    path("personal-customer/", personalCustomerView, name="personal-customer"),
    path("business-customer/", businessCustomerView, name="business-customer"),

    # Admin customer
    path("admin-customer-edit/<int:shop_id>/<int:cust_id>/", adminEditCustomerView, name="admin-customer-edit"),

    # vendor
    path("vendor/<int:shop_id>/", vendorView, name="vendor"),
    path("edit-vendor/<int:shop_id>/<int:vendor_id>/", editVendorView, name="edit-vendor"),
    path("create-vendor/<shop_id>/", createVendorView, name="create-vendor"),
    path("delete-vendor/<int:shop_id>/<int:vendor_id>/", deleteVendorView, name="delete-vendor"),

    # employee
    path("employee/<int:shop_id>/", employeeView, name="employeeView"),
    path("create-employee/<int:shop_id>/", createEmployeeView, name="createEmployeeView"),
    path("edit-employee/<int:emp_id>/<int:shop_id>/", editEmployeeView, name="edit-employee"),
    path("delete-employee/<int:emp_id>/<int:shop_id>/", deleteEmployeeView, name="deleteEmployeeView"),


    # settings
    path("contact/<int:shop_id>/", contactView, name="contact"),
    path("submit-contact/<int:shop_id>/", submitContact, name="submit-contact"),

    # Exception
    # success
    path("success/", successView, name="success"),  

    # failed  
    path("failed/", failedView, name="failed"),
    # not found  
    path("notFound/", notFoundView, name="notFound"),
     # warning  
    path("warning/", warningView, name="warning"),


    # Export
    path("export-customer-data/<int:shop_id>/", exportCustomerData, name="export-customer-data"),
    path("export-product-data/<int:shop_id>/", exportProductData, name="export-product-data"),

    # Create table
    path("create-table/<int:shop_id>/", createTable, name="create-table"),
    path("admin-create-table/<int:shop_id>/", adminCreateTableView, name="admin-create-table"),
    path("all-tables/<int:shop_id>/", allTablesView, name="admin-all-tables"),
    path("admin-delete-table/<int:shop_id>/<int:table_id>/", deleteTableView, name="admin-delete-table"),
    path("edit-table/<int:shop_id>/<int:table_id>/", editTableView, name="edit-table"),
    path("admin-edit-table/<int:shop_id>/<int:table_id>/", adminEditTableView, name="admin-edit-table"),


    # Role URL
    path("roles/<int:shop_id>/", roleViews, name="roleViews"),
    path("create-roles/<int:shop_id>/", createRolesView, name="createRolesView"),
    path("edit-roles/<int:role_id>/<int:shop_id>", editRolesView, name="editRolesView"),
    path("delete-roles/<int:role_id>/<int:shop_id>/", deleteRolesView, name="deleteRolesView"),

    # Shop settings
    path("shop-settings/<int:shop_id>/", viewShopSettings, name="shop-settings"),
    path("update-shop/<int:shop_id>/", updateShopSettings, name="update-shop"),

    path("due-orders/<int:shop_id>/", adminDueOrdersView, name="admin-due-orders"),
    path("table-orders/<int:shop_id>/", adminTableOrdersView, name="admin-table-orders"),
    path("advance-orders/<int:shop_id>/", adminAdvancedOrdersView, name="admin-advance-orders"),

    path("export-due-data/<int:shop_id>/", exportDueData, name="export-due-data"),
    path("export-table-checkout-data/<int:shop_id>/", exportTableCheckoutData, name="export-table-checkout-data"),
    path("export-advance-order-data/<int:shop_id>/", exportAdvanceBookingData, name="export-advance-order-data"),
]
