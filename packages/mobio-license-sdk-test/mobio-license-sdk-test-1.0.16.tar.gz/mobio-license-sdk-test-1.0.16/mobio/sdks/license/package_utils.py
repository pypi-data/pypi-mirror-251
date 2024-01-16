from .date_utils import convert_timestamp_to_date_utc, convert_date_to_timestamp, get_utc_now


class PackageUtils:
    class LicenseJson:
        merchant_id = "merchant_id"
        version = "version"
        created_time = "created_time"
        api_key = "api_key"
        alert_merchant = "alert_merchant"
        packages = "packages"
        field_map_module = "field_map_module"
        # start_time = "start_time"
        # expire_time = "expire_time"

    class LicenseMerchant:
        merchant_id = "merchant_id"
        packages = "packages"
        gift = "gift"
        currency_unit = "currency_unit"
        start_time = "start_time"
        active_time = "active_time"
        expire_time = "expire_time"
        module = "module"
        package_code = "package_code"
        total_specifications = "total_specifications"

    class PackageModule:
        cdp = "cdp"
        sales = "sales"
        services = "services"
        all_value = [cdp, sales, services]

    class PackageCode:
        free = "free"
        growth = "growth"
        professional = "professional"
        enterprise = "enterprise"
        enterprise_plus = "enterprise_plus"
        all_value = [free, growth, professional, enterprise, enterprise_plus, ]

    class Package:
        # package_code = "package_code"
        # module = "module"
        package_type = "package_type"
        attribute_calculate = "attribute_calculate"
        config_calculate = "config_calculate"
        package_parameters = "package_parameters"

        class Attribute:
            allow = "allow"
            attribute_type = "attribute_type"
            max = "max"
            min = "min"

        class AttributeType:
            quantity = "quantity"
            feature = "feature"

    def __init__(self, json_license: dict):
        self.json_license = json_license
        self.package_current = {}
        self.uncheck_license = False

        self.field_map_module = {
            "workflow_setup": [self.PackageModule.sales, self.PackageModule.services],
            "product_count": [self.PackageModule.sales, self.PackageModule.services],
        }
        if json_license and isinstance(json_license, dict):
            if json_license.get(self.LicenseJson.field_map_module):
                self.field_map_module = json_license.get(self.LicenseJson.field_map_module)

    def get_license_package_by_module(self, module):
        self.validate_module(module=module)
        try:
            if self.json_license and isinstance(self.json_license, dict):
                packages = self.json_license.get(self.LicenseJson.packages)
                if packages and isinstance(packages, list):
                    for item in packages:
                        module_item = item.get(self.LicenseMerchant.module)
                        if module != module_item:
                            continue
                        active_time = item.get(self.LicenseMerchant.active_time)
                        expire_time = item.get(self.LicenseMerchant.expire_time)
                        time_stamp_now = convert_date_to_timestamp(get_utc_now())
                        if active_time <= time_stamp_now < expire_time:
                            self.package_current[module] = item
                            break
            else:
                # sau nay kiem tra theo vmtype
                self.uncheck_license = True
        except Exception as e:
            print("license_sdk::get_license_package_by_module: ERROR: %s" % e)
        return self.package_current.get(module)

    def validate_module(self, module: str):
        if module not in self.PackageModule.all_value:
            raise ValueError("{} module invalid".format(module))

    def check_allow_attribute_quantity(self, module: str, attribute: str, number_check: int):
        data_package = {"is_allowed": False}
        package_module = self.get_license_package_by_module(module)
        if self.uncheck_license:
            return {
                "is_allowed": True,
                # "uncheck_license": True,
                # self.LicenseMerchant.package_code: self.PackageCode.enterprise_plus
            }
        if package_module and isinstance(package_module, dict):
            data_package.update({
                self.LicenseMerchant.module: module,
                self.LicenseMerchant.start_time: package_module.get(self.LicenseMerchant.start_time),
                self.LicenseMerchant.expire_time: package_module.get(self.LicenseMerchant.expire_time),
                self.LicenseMerchant.package_code: package_module.get(self.LicenseMerchant.package_code),
            })
            if package_module.get(self.LicenseMerchant.package_code) == self.PackageCode.enterprise_plus:
                data_package.update({"is_allowed": True})
                return data_package
            # else: # -1 la ko gioi han du bat ky goi nao

            data_attribute = package_module.get(self.LicenseMerchant.packages, {}).get(
                self.Package.package_parameters, {}).get(attribute, {})
            if (data_attribute and data_attribute.get(
                    self.Package.Attribute.attribute_type) == self.Package.AttributeType.quantity):
                if data_attribute.get(self.Package.Attribute.allow):
                    if attribute == package_module.get(self.LicenseMerchant.packages,
                                                       {}).get(self.Package.attribute_calculate):
                        number_package = package_module.get(self.LicenseMerchant.total_specifications)
                    else:
                        number_package = data_attribute.get(self.Package.Attribute.max, 0)
                    if number_package < 0 or number_check <= number_package:
                        data_package.update({"is_allowed": True})
                    else:
                        data_package.update({"max": number_package})
                # else:
                #     data_package.update({"is_allowed": True})
        return data_package

    def check_allow_attribute_feature(self, module: str, attribute: str):
        data_package = {"is_allowed": False}
        package_module = self.get_license_package_by_module(module)
        if self.uncheck_license:
            return {
                "is_allowed": True,
                "uncheck_license": True,
                # self.LicenseMerchant.package_code: self.PackageCode.enterprise_plus
            }
        if package_module and isinstance(package_module, dict):
            data_package.update({
                self.LicenseMerchant.module: module,
                self.LicenseMerchant.start_time: package_module.get(self.LicenseMerchant.start_time),
                self.LicenseMerchant.expire_time: package_module.get(self.LicenseMerchant.expire_time),
                self.LicenseMerchant.package_code: package_module.get(self.LicenseMerchant.package_code),
            })
            if package_module.get(self.LicenseMerchant.package_code) == self.PackageCode.enterprise_plus:
                data_package.update({"uncheck_license": True, "is_allowed": True})
                return data_package
            data_attribute = package_module.get(self.LicenseMerchant.packages, {}).get(
                self.Package.package_parameters, {}).get(attribute, {})
            if (data_attribute and data_attribute.get(
                    self.Package.Attribute.attribute_type) == self.Package.AttributeType.feature):
                data_package.update(data_attribute)
                if data_attribute.get(self.Package.Attribute.allow):
                    data_package.update({"is_allowed": True})
        return data_package

    def get_attribute_quantity(self, module: str, attribute: str):
        data_package = {"unlimited": False}
        package_module = self.get_license_package_by_module(module)
        if self.uncheck_license:
            return {
                "unlimited": True
                # "is_allowed": True,
                # "uncheck_license": True,
                # self.LicenseMerchant.package_code: self.PackageCode.enterprise_plus
            }
        if package_module and isinstance(package_module, dict):
            data_package.update({
                self.LicenseMerchant.module: module,
                self.LicenseMerchant.start_time: package_module.get(self.LicenseMerchant.start_time),
                self.LicenseMerchant.expire_time: package_module.get(self.LicenseMerchant.expire_time),
                self.LicenseMerchant.package_code: package_module.get(self.LicenseMerchant.package_code),
            })
            if package_module.get(self.LicenseMerchant.package_code) == self.PackageCode.enterprise_plus:
                data_package.update({"unlimited": True})
                return data_package

            data_attribute = package_module.get(self.LicenseMerchant.packages, {}).get(
                self.Package.package_parameters, {}).get(attribute, {})
            if (data_attribute and data_attribute.get(
                    self.Package.Attribute.attribute_type) == self.Package.AttributeType.quantity):
                if data_attribute.get(self.Package.Attribute.allow):
                    if attribute == package_module.get(self.LicenseMerchant.packages,
                                                       {}).get(self.Package.attribute_calculate):
                        number_package = package_module.get(self.LicenseMerchant.total_specifications)
                    else:
                        number_package = data_attribute.get(self.Package.Attribute.max, 0)
                    if number_package < 0:
                        data_package.update({"unlimited": True})
                    else:
                        data_package.update({"max": number_package})
                # else:
                #     data_package.update({"is_allowed": True})
        return data_package

    def pre_check_allow_attribute_quantity(self, module: str, attribute: str, number_check: int):
        if attribute in self.field_map_module:
            data_default = {"is_allowed": False}
            number_max = None
            for m in self.field_map_module.get(attribute):
                data_package = self.check_allow_attribute_quantity(
                    module=m, attribute=attribute, number_check=number_check
                )
                if data_package:
                    if data_package.get("is_allowed"):
                        return data_package
                    else:
                        data_default.update(data_package)
                        if "max" in data_package:
                            if number_max is None or number_max < data_package.get("max"):
                                number_max = data_package.get("max")
            if number_max is not None:
                data_default.update({"max": number_max})
            return data_default
        else:
            return self.check_allow_attribute_quantity(
                module=module, attribute=attribute, number_check=number_check
            )

    def pre_get_attribute_quantity(self, module: str, attribute: str):
        if attribute in self.field_map_module:
            data_default = {"unlimited": False}
            number_max = None
            for m in self.field_map_module.get(attribute):
                data_package = self.get_attribute_quantity(
                    module=m, attribute=attribute
                )
                if data_package:
                    if data_package.get("unlimited"):
                        return data_package
                    else:
                        data_default.update(data_package)
                        if "max" in data_package:
                            if number_max is None or number_max < data_package.get("max"):
                                number_max = data_package.get("max")
            if number_max is not None:
                data_default.update({"max": number_max})
            return data_default
        else:
            return self.get_attribute_quantity(
                module=module, attribute=attribute
            )

    def pre_check_allow_attribute_feature(self, module: str, attribute: str):
        if attribute in self.field_map_module:
            data_default = {"is_allowed": False}
            for m in self.field_map_module.get(attribute):
                data_package = self.check_allow_attribute_feature(
                    module=m, attribute=attribute
                )
                if data_package:
                    if data_package.get("is_allowed"):
                        return data_package
                    else:
                        data_default.update(data_package)
            return data_default
        else:
            return self.check_allow_attribute_feature(
                module=module, attribute=attribute
            )

    @classmethod
    def calculate_limit_number(cls, number_mtp):
        return {
            "mtp": number_mtp,
            "message": number_mtp * 10,
        }

    def get_limit_activation_cdp(self):
        data_package = {
            "unlimited": False,
            "mtp": 0,
            "message": 0,
        }
        package_module = self.get_license_package_by_module(self.PackageModule.cdp)
        if self.uncheck_license:
            data_package.update({"unlimited": True})
            return data_package
        if package_module and isinstance(package_module, dict):
            data_package.update({
                self.LicenseMerchant.module: self.PackageModule.cdp,
                self.LicenseMerchant.start_time: package_module.get(self.LicenseMerchant.start_time),
                self.LicenseMerchant.expire_time: package_module.get(self.LicenseMerchant.expire_time),
                self.LicenseMerchant.package_code: package_module.get(self.LicenseMerchant.package_code),
            })
            number_mtp = package_module.get(self.LicenseMerchant.total_specifications, 0)
            if package_module.get(self.LicenseMerchant.package_code) == self.PackageCode.free:
                data_package.update(self.calculate_limit_number(number_mtp))
            else:
                data_package.update({"unlimited": True})
                # lay thong tin time gift free
                if (package_module.get(self.LicenseMerchant.gift) and
                        isinstance(package_module.get(self.LicenseMerchant.gift), dict)):
                    gift_info = package_module.get(self.LicenseMerchant.gift)
                    if gift_info.get("start_free") and gift_info.get("end_free"):
                        time_stamp_now = convert_date_to_timestamp(get_utc_now())
                        if gift_info.get("start_free") <= time_stamp_now < gift_info.get("end_free"):
                            data_package.update({"unlimited": False})
                            data_package.update(self.calculate_limit_number(number_mtp))
        return data_package


if __name__ == "__main__":
    json_package = {
        "packages": {
            "sales": {
                "packages": {
                    "package_code": "enterprise",
                    "module": "sales",
                    "status": "active",
                    "package_type": "fix",
                    "attribute_calculate": "number_user",
                    "config_calculate": [
                        {
                            'start': 11,
                            'end': 1000,
                            'price': {
                                'vnd': 1_000_000,
                                'usd': 40
                            },
                            'per': 1
                        },
                    ],
                    "price_base": {
                        "vnd": 10_000_000,
                        "usd": 400,
                    },
                    "package_parameters": {
                        "number_user": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': 1000,
                            'min': 10,
                        },
                        "admin_team": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                        "deal_dynamic_field": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                        "media_storage": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': 10,
                        },
                        "deal_pipeline_setup": {
                            "allow": 1,
                            "attribute_type": "quantity",
                            'max': -1,
                        },
                    },
                },
                "expire_time": 2592442000,
            }
        }
    }
    # result = PackageUtils(json_license=json_package).check_allow_attribute_quantity(
    #     module="sales", attribute="number_user", number_check=1001
    # )
    result = PackageUtils(json_license=json_package).check_allow_attribute_feature(
        module="sales", attribute="number_user"
    )
    print(result)
