export function hasRole(user, role) {
  if (!user || !user.roles) return false;
  return user.roles.includes(role);
}
