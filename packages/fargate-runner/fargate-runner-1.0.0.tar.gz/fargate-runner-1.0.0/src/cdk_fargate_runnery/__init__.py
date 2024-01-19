'''
# replace this
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import constructs as _constructs_77d1e7e8


class FargateRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="fargate-runner.FargateRunner",
):
    '''
    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        fargate_task_def: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        count: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param fargate_task_def: 
        :param count: 
        :param timeout: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69cbcb0ae200b9ad446b494def616317239148b1ad42439e76cd184ab00b4e93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateRunnerProps(
            fargate_task_def=fargate_task_def, count=count, timeout=timeout, vpc=vpc
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="waitCondition")
    def wait_condition(self) -> _aws_cdk_ceddda9d.CfnWaitCondition:
        '''
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.CfnWaitCondition, jsii.get(self, "waitCondition"))


@jsii.data_type(
    jsii_type="fargate-runner.FargateRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "fargate_task_def": "fargateTaskDef",
        "count": "count",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class FargateRunnerProps:
    def __init__(
        self,
        *,
        fargate_task_def: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        count: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[builtins.str] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    ) -> None:
        '''
        :param fargate_task_def: 
        :param count: 
        :param timeout: 
        :param vpc: 

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b023cfac9d42abff7d577177c1092989237d58aa288378ba3fb2bda55b1df54f)
            check_type(argname="argument fargate_task_def", value=fargate_task_def, expected_type=type_hints["fargate_task_def"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "fargate_task_def": fargate_task_def,
        }
        if count is not None:
            self._values["count"] = count
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def fargate_task_def(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        '''
        :stability: experimental
        '''
        result = self._values.get("fargate_task_def")
        assert result is not None, "Required property 'fargate_task_def' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[builtins.str]:
        '''
        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''
        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "FargateRunner",
    "FargateRunnerProps",
]

publication.publish()

def _typecheckingstub__69cbcb0ae200b9ad446b494def616317239148b1ad42439e76cd184ab00b4e93(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    fargate_task_def: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    count: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b023cfac9d42abff7d577177c1092989237d58aa288378ba3fb2bda55b1df54f(
    *,
    fargate_task_def: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    count: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[builtins.str] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
) -> None:
    """Type checking stubs"""
    pass
