from typing import TypedDict, Literal

from alibabacloud_tea_openapi.models import Config as SessionConfig

from .tea_api import AliCloudTeaApi


class SecurityGroupRuleSchema(TypedDict):
    SourceGroupId: str | None
    Policy: Literal["Accept", "Drop"]
    Description: str | None
    SourceCidrIp: str | None
    SourcePortRange: str | None
    Priority: int | None
    DestPrefixListName: str | None
    Ipv6SourceCidrIp: str | None
    NicType: Literal["intranet", "intranet"]
    Direction: Literal["ingress", "egress", "all"]
    DestGroupId: str | None
    SourceGroupName: str | None
    PortRange: str | None
    DestGroupOwnerAccount: str | None
    DestPrefixListId: str | None
    SourcePrefixListName: str | None
    IpProtocol: Literal["TCP", "UDP", "ICMP", "ICMP6", "GRE", "ALL"]
    SecurityGroupRuleId: str | None
    DestCidrIp: str | None
    DestGroupName: str | None
    Ipv6DestCidrIp: str | None
    SourceGroupOwnerAccount: str | None
    SourcePrefixListId: str | None


class SecurityGroupManager(AliCloudTeaApi):
    def __init__(self, config: SessionConfig, region="cn-shanghai"):
        self.region = region
        super().__init__(config, "2014-05-26", endpoint=f"ecs.{region}.aliyuncs.com")

    def get_sg_rules(self, sg_id: str, direction="all", nic_type="internet") -> list[SecurityGroupRuleSchema]:
        """
        :param sg_id:
        :param direction: all | ingress | egress
        :param nic_type: internet | intranet
        :return:
        """
        return self.call_api(
            action="DescribeSecurityGroupAttribute",
            queries={
                "SecurityGroupId": sg_id,
                "RegionId": self.region,
                "NicType": nic_type,
                "Direction": direction
            }
        )['Permissions']['Permission']

    def delete_rules(self, sg_id: str, rule_ids: list[str]):
        return self.call_api(
            action="RevokeSecurityGroup",
            queries={
                "SecurityGroupId": sg_id,
                "RegionId": self.region,
                "SecurityGroupRuleId": rule_ids
            }
        )

    def create_rules(self, sg_id: str, rules: list[SecurityGroupRuleSchema]) -> list:
        """
        create security group rule, if rule already exists,skip,no update will be performed
        """
        queries = {
            "RegionId": self.region,
            "SecurityGroupId": sg_id,
        }
        for no, rule in enumerate(rules):
            for k, v in rule.items():
                queries[f"Permissions.{no + 1}.{k}"] = v
        return self.call_api(
            action="AuthorizeSecurityGroup",
            queries=queries
        )
