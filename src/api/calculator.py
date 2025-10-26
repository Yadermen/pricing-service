from fastapi import APIRouter, HTTPException, status

from src.repositories.project import ProjectCRUD
from src.repositories.project_role import ProjectRoleCRUD
from src.repositories.role import RoleCRUD
from src.services.calculator import calculate_cost

router = APIRouter(prefix="/calculator", tags=["Calculator"])


@router.get(
    "/projects/{project_id}/calculate",
    summary="Calculate project cost",
    description="Calculate the total cost for a project based on roles and coefficients"
)
async def calculate_project_cost(project_id: int):

    project = await ProjectCRUD.get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    project_roles = await ProjectRoleCRUD.get_project_roles_by_project_id(project_id)
    if not project_roles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No roles found for this project"
        )

    team_roles = []
    for pr in project_roles:
        role = await RoleCRUD.get_role_by_id(pr.role_id)
        if not role:
            continue

        team_roles.append({
            "count": pr.count,
            "rate": pr.custom_rate if pr.custom_rate is not None else role.default_rate
        })


    coefficients = [project.coefficient]

    total_price = calculate_cost(team_roles, coefficients)
    if total_price > 2000000000:
        total_price = 2000000000
    await ProjectCRUD.set_project_price(project.id, total_price)

    return {
        "project": project,
        "total_price": total_price
    }