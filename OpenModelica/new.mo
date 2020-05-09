model new
  Modelica.Blocks.Sources.Pulse pulse(amplitude = 3000, nperiod = 1, offset = 0, period = 5000, startTime = 10, width = 80)  annotation(
    Placement(visible = true, transformation(origin = {-86, 0}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.FirstOrder firstOrder(T = 500)  annotation(
    Placement(visible = true, transformation(origin = {-50, 60}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Continuous.Integrator integrator(k = 0.001)  annotation(
    Placement(visible = true, transformation(origin = {-36, -42}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
  Modelica.Blocks.Math.Add add annotation(
    Placement(visible = true, transformation(origin = {52, 2}, extent = {{-10, -10}, {10, 10}}, rotation = 0)));
equation
  connect(integrator.u, pulse.y) annotation(
    Line(points = {{-48, -42}, {-74, -42}, {-74, 0}}, color = {0, 0, 127}));
  connect(firstOrder.u, pulse.y) annotation(
    Line(points = {{-62, 60}, {-74, 60}, {-74, 0}}, color = {0, 0, 127}));
  connect(add.u2, integrator.y) annotation(
    Line(points = {{40, -4}, {-19.5, -4}, {-19.5, -42}, {-25, -42}}, color = {0, 0, 127}));
  connect(add.u1, firstOrder.y) annotation(
    Line(points = {{40, 8}, {-22.5, 8}, {-22.5, 60}, {-39, 60}}, color = {0, 0, 127}));
  annotation(
    uses(Modelica(version = "3.2.3")));
end new;
