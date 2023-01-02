# define custom filters
from django import template

register = template.Library()

@register.filter
def org_role(user, org_id):
    
    member_role =  user.organizationmember_set.filter(organization_id=org_id)
    if member_role.exists():
        member_role = member_role.first().role
    else:
        member_role = 'member'
    # if user is owner of the organization, return owner
    if user.organization_set.filter(id=org_id, owner=user).exists():
        member_role = 'owner'
        
    return member_role

@register.simple_tag
def org_role_stage(user, org_id, stage_role):

    member_role =  user.organizationmember_set.filter(organization_id=org_id)
    if member_role.exists():
        member_role = member_role.first().role
    else:
        member_role = 'member'
    
    # if user is owner of the organization, return owner
    if user.organization_set.filter(id=org_id, owner=user).exists():
        member_role = 'owner'
        
    if member_role == 'owner':
        return True
    
    if member_role == 'admin' and stage_role in ['member', 'admin']:
        return True
    
    if member_role == 'member' and stage_role == 'member':
        return True
    
    return False