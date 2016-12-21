# coding: utf-8
#
# Solving Helmhotz equation with FEniCS
# Author: Juan Luis Cano Rodríguez <juanlu@pybonacci.org>
# Inspired by: http://jasmcole.com/2014/08/25/helmhurts/
#https://fenicsproject.org/olddocs/dolfin//1.3.0/python/demo/documented/neumann-poisson/python/documentation.html
#https://fenicsproject.org/olddocs/dolfin//1.3.0/python/demo/documented/singular-poisson/python/documentation.html
import sys
import numpy as np
from dolfin import *
from fenics import *
from mshr import *
from math import fabs


def helmgoltz_1(u_D, f, alpha):
    ## Formulation
    
    
    print(333)
    print("f",f)
    print("a", alpha)
    print("u_D",u_D)
    #u_D = Expression('sin(x[0]) * cos(x[1])', degree=2)
    #g = Expression('-sin(x[0] * cos(x[1]))', degree=2)
    
    # Boundary conditions
    def boundary(x, on_boundary):
        return on_boundary 

    bc = DirichletBC(V, u_D, boundary)

    # Equation
    u = TrialFunction(V)
    v = TestFunction(V)
    a = (alpha*inner(u, v) + inner(nabla_grad(u), nabla_grad(v))) * dx

    L = f*v*dx

    # Solve system
    u = Function(V)
    solve(a == L, u, bc)

    # error 
    error_L2 = errornorm(u_D, u, 'L2')
    vertex_values_u_D = u_D.compute_vertex_values(mesh)
    vertex_values_u = u.compute_vertex_values(mesh)
    error_C = np.max(np.abs(vertex_values_u - vertex_values_u_D))
    print("L2_error=", error_L2)
    print("C_error=", error_C)

        
    # Plot and export solution
    plot(u, interactive=True)
    #plot(mesh)
    file = File("helmhurts.pvd")
    file << u
    return u

def helmgoltz_2(u_D, f, g, alpha):
    tol = 1E-3

    #u_D = Expression('sin(x[0]) * cos(x[1])', degree=2)
    #g = Expression('cos(x[0]) * cos(x[1]) - sin(x[0])*sin(x[1])', degree=2)
    #f = Constant(0.0)

    def boundary_D(x, on_boundary):
	return on_boundary and fabs(x[0]*x[0]+x[1]*x[1]-1.0) < tol
	
    bc = DirichletBC(V, u_D, boundary_D)

    # Equation
    u = TrialFunction(V)
    v = TestFunction(V)
    a = (alpha*inner(u, v) + inner(nabla_grad(u), nabla_grad(v))) * dx
    L = f*v*dx - g*v*ds

    # Solve system
    u = Function(V)
    solve(a == L, u, bc)

    # error 
    error_L2 = errornorm(u_D, u, 'L2')
    vertex_values_u_D = u_D.compute_vertex_values(mesh)
    vertex_values_u = u.compute_vertex_values(mesh)
    error_C = np.max(np.abs(vertex_values_u - vertex_values_u_D))
    print("L2_error=", error_L2)
    print("C_error=", error_C)
        
    # Plot and export solution
    plot(u, interactive=True)
    #plot(mesh)
    file = File("helmhurts2.pvd")
    file << u
    return u

def heat_equation_1():
    T = 2.0
    num_steps = 2
    dt = T/num_steps
    alpha = 3
    beta = 1.2
    t=0
    global V
    u_0 = Expression('1 + x[0]*x[0] + alpha*x[1]*x[1]',
degree=2, alpha=alpha, beta=beta)
    loc_f = u_0/dt+beta-2-2*alpha
    for i in range(num_steps):
	t+=dt
	sol = helmgoltz_1(Expression('1 + x[0]*x[0] + alpha*x[1]*x[1] + beta*t', alpha=alpha, beta=beta, t=t, degree=2),loc_f, 1/dt)
	loc_f = interpolate(sol,V)/dt+beta-2-2*alpha

def heat_equation_2():
    T = 2.0
    num_steps = 2
    dt = T/num_steps
    alpha = 3
    beta = 1.2
    t=0
    u_0 = Expression('1 + x[0]*x[0] + alpha*x[1]*x[1]',
degree=2, alpha=alpha, beta=beta)
    loc_f = u_0/dt+beta-2-2*alpha
    for i in range(num_steps):
	t+=dt
	sol = helmgoltz_2(Expression('1 + x[0]*x[0] + alpha*x[1]*x[1] + beta*t', alpha=alpha, beta=beta, t=t, degree=2),loc_f, 2+2*alpha, 1/dt)
	loc_f = interpolate(sol,V)/dt+beta-2-2*alpha



if __name__ == '__main__':
    flag = int(sys.argv[1])
    domain = Circle(Point(0.0,0.0),1.0)
    mesh = generate_mesh(domain, 64)
    V = FunctionSpace(mesh, 'P', 1)
    if flag == 1:
        helmgoltz_1(Expression('sin(x[0]) * cos(x[1])', degree=2),Expression('sin(x[0]) * cos(x[1])', degree=2), 2)
    if flag == 2:
        helmgoltz_2()
    if flag == 3:
        heat_equation_1()
    if flag == 4:
        heat_equation_2()

